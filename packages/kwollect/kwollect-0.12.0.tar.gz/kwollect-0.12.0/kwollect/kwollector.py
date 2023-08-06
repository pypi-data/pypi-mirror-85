#!/usr/bin/python3

import sys
import time
import re
import random
import asyncio
import aiohttp
import glob
import json
import traceback
import logging as log

import dataclasses
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse, unquote

import yaml
import aiopg
import psycopg2
import aiosnmp
from pyonf import pyonf


config = """
metrics_dir: /etc/kwollect/metrics.d/
db_host: localhost
db_name: kwdb
db_user: kwuser
db_password: changeme
log_level: warning
"""
config = pyonf(config)

log.basicConfig(
    level=str.upper(config.get("log_level", "warning")),
    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
)


def main():
    asyncio.run(async_main(), debug=config.get("log_level") == "debug")


async def async_main():

    await init_http()
    await init_psql()

    metrics = load_metric_descriptions(config["metrics_dir"])
    metrics_per_device = merge_metrics_per_device_and_protocol(metrics)
    metrics_per_device = await parse_snmp_template_metrics(metrics_per_device)

    for device, metrics in metrics_per_device.items():
        if device.protocol == "snmp":
            process_method = process_snmp_host
        elif device.protocol == "ipmisensor":
            process_method = process_ipmisensor_host
        elif device.protocol == "prometheus":
            process_method = process_prometheus_host
        else:
            log.error("Unsupported protocol for device %s", device)
            continue

        req_interval_ms = min(metric.update_every for metric in metrics)

        log.info(
            "Scheduling %s requests every %s milli-seconds", device, req_interval_ms
        )
        asyncio.create_task(
            schedule_every(
                req_interval_ms / 1000,
                process_method,
                (device, metrics),
                task_name=f"{device.protocol}@{device.hostname}",
            )
        )

    # Waiting for infinity, but catching failing tasks
    ended_task, _ = await asyncio.wait(
        asyncio.all_tasks(), return_when=asyncio.FIRST_COMPLETED
    )
    log.critical("Scheduler task %s as ended, that should not happen", ended_task)
    sys.exit(1)


@dataclass(frozen=True)
class MetricDevice:
    """A device to be queried by some protocol"""

    hostname: str
    protocol: str
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None


@dataclass
class MetricDescription:
    """A metrics to fetch"""

    name: str
    device_id: str
    url: str
    path: str = ""
    update_every: int = 10000
    optional: bool = False
    labels: Optional[dict] = None
    scale_factor: Optional[float] = None

    def __post_init__(self):
        _url = urlparse(self.url)
        self.device = MetricDevice(
            hostname=_url.hostname,
            protocol=_url.scheme,
            port=_url.port,
            username=unquote(_url.username) if _url.username else None,
            password=unquote(_url.password) if _url.password else None,
        )
        if _url.path:
            self.path = re.sub(r"^/", "", unquote(_url.path))


def load_metric_descriptions(metrics_dir):
    """Load metric descriptions from directory"""
    log.debug("Loading metric descriptions from %s", metrics_dir)
    metrics = []
    for description_file in glob.glob(metrics_dir + "/*"):
        with open(description_file) as f:
            try:
                ydata = yaml.safe_load(f.read())
                if isinstance(ydata, list):
                    metrics += [MetricDescription(**d) for d in ydata]
                elif isinstance(ydata, dict):
                    metrics.append(MetricDescription(**ydata))
                elif ydata is None:
                    pass
                else:
                    raise Exception("Unparsable metric description")
            except Exception as ex:
                log.error("Error when reading %s content", description_file)
                log.error("%s: %s", repr(ex), str(ex))
                log.error(traceback.format_exc())
                sys.exit(1)

    log.debug("\n  ".join((str(metric) for metric in metrics)))
    return metrics


def merge_metrics_per_device_and_protocol(metrics):
    """Merge list of metrics per involved device and returns a Dict[MetricDevice, MetricDescription]"""
    metrics_per_device = {}
    for metric in metrics:
        if metric.device not in metrics_per_device:
            metrics_per_device[metric.device] = []
        metrics_per_device[metric.device].append(metric)
    return metrics_per_device


async def schedule_every(
    period, func_name, args=[], kwargs={}, delayed_start=True, task_name=None
):
    """Schedule func_name to run every period"""

    TIMEOUT_MAX_COUNT = 5

    if not task_name:
        task_name = (
            f"{func_name}("
            + ", ".join(args)
            + ", "
            + ", ".join(f"{k}={v}" for k, v in kwargs.items())
        )

    if delayed_start and period > 1:
        await asyncio.sleep(random.randint(0, int(period * 1000)) / 1000)

    log.debug("Start task scheduler for %s", task_name)

    while True:

        task = asyncio.create_task(func_name(*args, **kwargs))
        task.task_name = task_name + "/" + str(int(time.time()))
        log.debug("Task created: %s", task.task_name)
        timeout_count = 0

        while True:
            await asyncio.sleep(period)
            if not task.done():
                timeout_count += 1
                if timeout_count >= TIMEOUT_MAX_COUNT:
                    log.error(
                        "Cancelling task that did not finished after %s periods of %s sec: %s",
                        TIMEOUT_MAX_COUNT,
                        period,
                        task.task_name,
                    )
                    task.cancel()
                    break
                log.warning(
                    "Waiting for task that did not finish under its period of %s sec: %s",
                    period,
                    task.task_name,
                )
            elif task.exception():
                log.error(
                    'Task had an exception %s ["%s"], scheduling new one: %s',
                    repr(task.exception()),
                    task.exception(),
                    task.task_name,
                )
                task.print_stack()
                break
            else:
                log.debug("Task correctly finished: %s", task.task_name)
                break


async def process_snmp_host(device, metrics):
    """Process one query for metrics on a device using SNMP"""

    log.debug(
        "Starting process_snmp_host for task: %s", asyncio.current_task().task_name
    )

    metrics = await filter_optional_metrics(metrics)
    if not metrics:
        log.info(
            "Nothing to process after filtering optional metrics for SNMP host %s",
            device.hostname,
        )
        return

    # "oids" maps SNMP OID with the associated metric position in "metrics" list
    # (the OID must be stored as string, without heading ".")
    oids = {metric.path: metric_idx for metric_idx, metric in enumerate(metrics)}

    # "results" stores SNMP request result and has same length and ordering than metrics
    # (None value is used if result is not available for a metric)
    results = [None] * len(metrics)

    timestamp = time.time()
    _results = await make_snmp_request(
        device.hostname, "get", list(oids.keys()), device.username
    )
    log.debug(
        "snmpget request executed in %s for task: %s",
        time.time() - timestamp,
        asyncio.current_task().task_name,
    )

    for oid, value in _results.items():
        results[oids[oid]] = value

    if not any(results):
        log.warning("Nothing to process for SNMP host %s", device.hostname)
        return

    values = [(timestamp, result) for result in results]
    await insert_metrics_values(metrics, values)


async def process_ipmisensor_host(device, metrics):
    """Process one query for metrics on a device using IPMI"""

    log.debug(
        "Starting process_ipmisensor_host for task: %s",
        asyncio.current_task().task_name,
    )

    metrics = await filter_optional_metrics(metrics)
    if not metrics:
        log.info(
            "Nothing to process after filtering optional metrics for IPMI host %s",
            device.hostname,
        )
        return

    timestamp = time.time()

    command = (
        f"/usr/sbin/ipmi-sensors --sdr-cache-recreate -D LAN_2_0 -h {device.hostname}"
    )
    if device.username:
        command += f" -u {device.username}"
    if device.password:
        command += f" -p '{device.password}'"
    # command += " -r " + ",".join(metric.path for metric in metrics)
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    log.debug(
        "ipmi-sensor command executed in %s for task: %s",
        time.time() - timestamp,
        asyncio.current_task().task_name,
    )

    if process.returncode != 0:
        log.error(
            "ipmi-sensor command %s failed for task: %s (%s)",
            command,
            asyncio.current_task().task_name,
            stderr,
        )
        return

    # parse ipmi-sensor stdout and store values by sensor name and sensor ID.
    # (both ipmi-sensor's ID and name fields may be used in the MetricDescription
    # URL path but some devices use identical names for different sensor, so ID is safer)
    ipmisensor_values = {}
    for ipmisensor_output in stdout.decode().strip().split("\n")[1:]:
        values = [value.strip() for value in ipmisensor_output.split("|")]
        sensor_id, sensor_name, sensor_value = values[0], values[1], values[3]
        ipmisensor_values[sensor_id] = sensor_value
        ipmisensor_values[sensor_name] = sensor_value

    # "results" stores IPMI result and has same length and ordering than metrics
    # (None value is used if result is not available for a metric)
    results = [None] * len(metrics)

    for metric_idx, sensor_name in enumerate(metric.path for metric in metrics):
        if sensor_name not in ipmisensor_values:
            log.warning(
                "Could not find IPMI sensor with name or ID %s on device %s",
                sensor_name,
                device.hostname,
            )
        elif ipmisensor_values[sensor_name] != "N/A":
            results[metric_idx] = ipmisensor_values[sensor_name]

    if not any(results):
        log.info(
            "Nothing to process for IPMI sensor host %s (guess: got N/A values only)",
            device.hostname,
        )
        return

    values = [(timestamp, result) for result in results]
    await insert_metrics_values(metrics, values)


async def process_prometheus_host(device, metrics):
    """Process one query for metrics on a prometheus exporter device"""

    log.debug(
        "Starting process_prometheus_host for task: %s",
        asyncio.current_task().task_name,
    )

    metrics = await filter_optional_metrics(metrics)
    if not metrics:
        log.info(
            "Nothing to process after filtering optional metrics for Prometheus host %s",
            device.hostname,
        )
        return

    timestamp = time.time()

    try:
        async with http_session.get(
            f"http://{device.hostname}:{device.port}/metrics"
        ) as resp:
            assert resp.status == 200
            resp_txt = await resp.text()
    except aiohttp.ClientConnectorError:
        log.warn(
            "Cannot connect to Prometheus host %s:%s, skipping",
            device.hostname,
            device.port,
        )
        log.debug(traceback.format_exc())
        return

    prom_re = re.compile(r"(\w+)({?.*}?) (.*)")
    promlabel_re = re.compile(r"(\w+)=\"(.*?)\"")

    fetched_metrics = []
    values = []

    for metric in metrics:

        # Metric to be fetched may limited to what's in path
        allowed_metrics = None
        if metric.path:
            allowed_metrics = metric.path.split("-")

        for prom_metric in resp_txt.strip().split("\n"):
            if not prom_metric.startswith("#"):
                (
                    prom_metric_name,
                    prom_metric_label_str,
                    prom_metric_value,
                ) = prom_re.match(prom_metric).groups()

                if allowed_metrics and not prom_metric_name in allowed_metrics:
                    continue

                fetched_metric = dataclasses.replace(
                    metric, name="prom_" + prom_metric_name
                )

                if prom_metric_label_str:
                    prom_metric_label = {
                        k: v for k, v in promlabel_re.findall(prom_metric_label_str)
                    }
                    if not fetched_metric.labels:
                        fetched_metric.labels = {}
                    fetched_metric.labels.update(prom_metric_label)

                custom_timestamp = None
                if fetched_metric.name == "prom_kwollect_custom":
                    if fetched_metric.labels.get("_metric_id"):
                        fetched_metric.name = fetched_metric.labels["_metric_id"]
                        del fetched_metric.labels["_metric_id"]
                        fetched_metric.labels["_metric_origin"] = "prom_kwollect_custom"
                    if fetched_metric.labels.get("_timestamp"):
                        custom_timestamp = fetched_metric.labels["_timestamp"]
                        del fetched_metric.labels["_timestamp"]
                        fetched_metric.labels["_metric_scrape_time"] = timestamp

                if not fetched_metric.name in [
                    existing_metric.name for existing_metric in fetched_metrics
                ]:
                    fetched_metrics.append(fetched_metric)
                    values.append((custom_timestamp or timestamp, prom_metric_value))

    if not any(fetched_metrics):
        log.info("Nothing to process for prometheus host %s", device.hostname)
        return

    await insert_metrics_values(fetched_metrics, values)


promoted_devices_and_metrics = []
promoted_lastupdate = -1


async def filter_optional_metrics(metrics):
    """Query DB to filter out optional metrics from metrics argument for a device"""
    global promoted_devices_and_metrics, promoted_lastupdate
    cur_time = int(time.time())
    if cur_time - promoted_lastupdate > 0:
        promoted_lastupdate = cur_time
        log.debug(
            "Prepare updating promoted devices for task: %s",
            asyncio.current_task().task_name,
        )
        promoted_devices_and_metrics = await sql(
            "SELECT device_id, metric_id FROM promoted_metrics", fetch=True
        )
    return [
        metric
        for metric in metrics
        if not metric.optional
        or any(
            [
                (
                    metric.device_id == promoted_device
                    or (
                        metric.labels
                        and metric.labels.get("_device_alias", "") == promoted_device
                    )
                )
                and re.match(rf"{promoted_metric}", metric.name)
                for promoted_device, promoted_metric in promoted_devices_and_metrics
            ]
        )
    ]


async def insert_metrics_values(metrics, values):
    """Insert metrics and associated values into DB"""

    sql_insert = (
        "INSERT INTO metrics(timestamp, device_id, metric_id, value, labels) VALUES\n  "
    )

    for i, metric in enumerate(metrics):
        timestamp, value = values[i]
        if value:
            sql_labels = {}
            sql_insert += f"(to_timestamp({timestamp}), "
            sql_insert += f"'{metric.device_id}', "
            sql_insert += f"'{metric.name}', "
            try:
                value = float(value)
                if metric.scale_factor:
                    value = value * metric.scale_factor
                sql_insert += f"{value}, "
            except ValueError:
                sql_insert += "'NaN', "
                sql_labels.update({"value_str": value})
            if metric.labels:
                sql_labels.update(metric.labels)
            sql_insert += f"'{json.dumps(sql_labels)}'"
            sql_insert += "),\n  "

    # Remove trailing '),\n  '
    sql_insert = sql_insert[:-4]

    log.debug(sql_insert)
    await sql(sql_insert)


async def parse_snmp_template_metrics(metrics_per_device):
    """Find real OID of SNMP metrics that use {{ oidprefix == value }} in their URLs"""

    parsed_metrics_per_device = {}

    # Parse metrics with SNMP {{ }} template in their URL
    for device, metrics in metrics_per_device.items():
        if device.protocol != "snmp":
            parsed_metrics_per_device[device] = metrics
        elif not any(
            metric for metric in metrics if re.findall(r"{{(.*)}}", metric.path)
        ):
            parsed_metrics_per_device[device] = metrics
        else:
            parsed_metrics_per_device[
                device
            ] = await parse_device_snmp_template_metrics(device, metrics)

    # Purge devices that don't have anymore metrics after parsing
    parsed_metrics_per_device = {
        device: metrics
        for device, metrics in parsed_metrics_per_device.items()
        if metrics
    }
    return parsed_metrics_per_device


async def parse_device_snmp_template_metrics(device, metrics):
    """Send SNMP request to retrieve OID suffixes corresponding to metrics' template"""

    def parse_template(metric):
        m = re.findall(r"{{(.*)==(.*)}}", metric.path)
        if m:
            return m[0][0].strip(), m[0][1].strip()

    results = {}
    for metric_oidprefix in set(
        parse_template(metric)[0] for metric in metrics if parse_template(metric)
    ):
        log.debug("Getting %s values on host %s", metric_oidprefix, device.hostname)
        results[metric_oidprefix] = await make_snmp_request(
            device.hostname,
            "walk",
            metric_oidprefix,
            device.username,
            timeout=20,
            retries=2,
        )

    for metric in metrics:
        if parse_template(metric):
            metric_oidprefix, metric_oidvalue = parse_template(metric)
            for oid, snmp_value in results.get(metric_oidprefix, {}).items():
                if snmp_value == metric_oidvalue:
                    oid_suffix = oid.replace(metric_oidprefix, "").strip(".")
                    metric.path = re.sub(r"{{.*}}", oid_suffix, metric.path)
                    log.debug("  %s is %s", metric_oidvalue, oid_suffix)

    new_metrics = []
    for metric in metrics:
        if re.findall(r"{{(.*)}}", metric.path):
            log.error(
                "SNMP template %s for %s not converted, deleting metrics",
                metric.path,
                device.hostname,
            )
        else:
            new_metrics.append(metric)
    log.debug(new_metrics)
    return new_metrics


http_session = None


async def init_http():
    global http_session
    http_session = aiohttp.ClientSession()


psql_pool = None


async def init_psql():
    global psql_pool
    psql_pool = await aiopg.create_pool(
        database=config["db_name"],
        user=config["db_user"],
        password=config["db_password"],
        host=config["db_host"],
        maxsize=75,
    )


async def sql(cmd, fetch=False):
    ret = []
    qtime = time.time()
    try:
        async with psql_pool.acquire() as conn:
            async with conn.cursor() as cur:
                log.debug(cur)
                log.debug(
                    "Got SQL worker after %s (free %s/%s) for task: %s",
                    time.time() - qtime,
                    psql_pool.freesize,
                    psql_pool.size,
                    asyncio.current_task().task_name,
                )
                qtime = time.time()
                await cur.execute(cmd)
                if fetch:
                    ret = await cur.fetchall()
    except psycopg2.OperationalError as ex:
        log.error("DB error on SQL request %s: %s", cmd[:6] + "...", ex)
        log.debug(traceback.format_exc())
    except psycopg2.ProgrammingError as ex:
        log.error("Error on SQL request %s", cmd)
        log.error(traceback.format_exc())
    except Exception as ex:
        log.error("Error when performing SQL command %s, abording", cmd)
        log.error(traceback.format_exc())
    log.debug(
        "Returing SQL %s after %s (free %s/%s) for task: %s",
        "SELECT" if fetch else "INSERT",
        time.time() - qtime,
        psql_pool.freesize,
        psql_pool.size,
        asyncio.current_task().task_name,
    )
    return ret


async def make_snmp_request(
    host, snmp_command, oids, community="public", timeout=30, retries=1
):
    """aiosnmp glue"""
    try:
        if snmp_command not in ("get", "walk"):
            raise Exception(f"Unsupported snmp_command (must be get or walk)")

        with aiosnmp.Snmp(
            host=host, port=161, community=community, timeout=timeout, retries=retries
        ) as snmp:
            if snmp_command == "get":
                # Slicing OIDs to perform SNMP GET with a maximum of 50 objects and avoid fragmentation
                snmp_results = []
                for oids_slice in (
                    oids[i : min(i + 50, len(oids))] for i in (range(0, len(oids), 50))
                ):
                    log.debug("snmp.get: %s %s", host, oids_slice)
                    snmp_results += await snmp.get(oids_slice)

            if snmp_command == "walk":
                if not isinstance(oids, str):
                    raise Exception(
                        f"Unsupported OID list for snmp_command walk (must be unique string)"
                    )
                log.debug("snmp.walk: %s %s", host, oids)
                snmp_results = await snmp.walk(oids)

        results = {}
        for res in snmp_results:
            results[str(res.oid).lstrip(".")] = (
                res.value.decode()
                if isinstance(res.value, (bytes, bytearray))
                else res.value
            )
        log.debug("snmp.results: %s", results)
        return results

    except asyncio.CancelledError:
        log.warning("Task cancelled when performing SNMP request, skipping...")
    except aiosnmp.exceptions.SnmpTimeoutError:
        log.error(
            "Timeout on SNMP request %s on %s %s, skipping...", snmp_command, host, oids
        )
    except Exception:
        log.error(
            "Error when performing SNMP request %s on %s with %s",
            snmp_command,
            host,
            oids,
        )
        log.error(traceback.format_exc())
    return {}


if __name__ == "__main__":
    main()
