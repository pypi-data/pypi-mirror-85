# Introduction

Kwollect is a framework for collecting metrics of IT infrastructures
(performance, environmental, ...) and make them available to users.

Kwollect targets high frequency collection with lossless & long term storage of
metrics and focuses on out-of-band metrics: those not available from computers
operating systems, but outside: sensors from PDUs, network devices, BMCs,
etc.

Kwollect is designed for integration with Job Schedulers, for instance when
deployed in High Performance Computing datacenters.


## Design Overview

Kwollect is a framework more than an individual software: It uses as many as
"on the shelf" components as possible.

In particular, it relies on a PostgreSQL database (with the TimescaleDB
extension) to store every metrics, provides the user API, and deal with the
backend "logic".

Some independent programs, called *kwollector*, collects the metrics from
various devices and store them in the database (currently supported protocols
are: SNMP, IPMI sensors, Prometheus exporter, OmegaWatt wattmetre).


# Usage

## Metrics format

Each metric data is associated with this information:
- *timestamp*: The date of the measurement
- *device_id*: The identifier of the device that is being measured
- *metric_id*: The name of the metric being measured
- *value*: The value of the metric when measurement is performed
- *labels*: Some arbitrary additional values, as JSON (e.g. an alternative name
  for the device)


## Querying metrics values

Kwollect provides an API to retrieve collected metrics:

```
curl 'http://kwollect.host:3000/rpc/get_metrics?devices=node-1,node-2&start_time=2020-01-06T13:35:00&end_time=2020-01-06T14:35:00'
```

It also provides a graphical view of metrics.

As it uses a PostgreSQL database, regular SQL queries can be used:

```
SELECT timestamp, device_id, metrics_id, values
  FROM metrics_by_device
  WHERE device_id = 'node-1' AND timestamp > now() - interval '1 hour';
```

## Inserting metrics values

In addition to the use of *kwollectors*, it is possible to manually insert so
metrics using the API:

```
curl http://kwollect.host:3000/rpc/insert_metrics \
  -H "Authorization: Bearer $TOKEN" \
  -H 'content-type: application/json' \
  -d '{"timestamp": "2020-01-06 14:00:00", "device_id": "node-1", "metric_id": "example_metric", "value": 42}'
```

Insertion requires the user to authenticate by providing an API token inside
`$TOKEN` variable (see API section below)

It is also possible to insert multiple metrics at a time:

```
curl http://kwollect.host:3000/rpc/insert_metrics \
  -H "Authorization: Bearer $TOKEN" \
  -H 'content-type: application/json' \
  -d '[
  {"device_id": "node-2", "metric_id": "example_metric1", "value": 42},
  {"device_id": "node-2", "metric_id": "example_metric2", "value": 22}
  ]'
```

An insertion may also be done using SQL under *metrics* table:

```
INSERT INTO metrics(timestamp, device_id, metric_id, value, labels)
  VALUES ('2020-01-06 14:00:00', 'node-3', 'example_metric', 42, '{"_device_alias": "node-3-admin"}')
```


# Installation

## Kwollect package

The kwollect package contains kwollector programs and database setup scripts. To install it, use:

```
pip3 install kwollect
```
(a Debian [package is also available](http://packages.grid5000.fr/deb/kwollect/))


## Database

Kwollect needs a [PostgreSQL](https://www.postgresql.org/) database with
[TimescaleDB](https://www.timescale.com/) extension to store metrics.

For example, use these commands to install them on Debian Buster:

```
sudo sh -c "echo 'deb https://packagecloud.io/timescale/timescaledb/debian/ `lsb_release -c -s` main' > /etc/apt/sources.list.d/timescaledb.list"
wget --quiet -O - https://packagecloud.io/timescale/timescaledb/gpgkey | sudo apt-key add -
sudo apt update
sudo apt-get install -y postgresql postgresql-client timescaledb-postgresql-11 postgresql-plpython3-11

# TimescaleDB comes with a script to tune Postgres configuration that you might want to use:
sudo cp /etc/postgresql/11/main/postgresql.conf /etc/postgresql/11/main/postgresql.conf-timescaledb_tune.backup
sudo timescaledb-tune -yes -quiet
echo 'timescaledb.telemetry_level=off' | sudo tee -a /etc/postgresql/11/main/postgresql.conf
sudo systemctl restart postgresql
```

Then, you can setup Kwollect database using the `kwollect-setup-db` tool. It is
required to connect to the database with administrator privileges. For instance:

```
sudo su postgres -s /bin/sh -c "kwollect-setup-db --kwollect_password changeme"
```

See `kwollect-setup-db --help` for more options. In particular,
*chunk_interval_hour* should be chosen such as all metrics collected during
this period, in hours, fits in the memory available to Postgres (about one quarter
of the entire memory, provided that one metric needs 200 bytes approx.)


## API

To provide an HTTP API to users to get metrics collected, kwollect uses
[Postgrest](http://postgrest.org).

These commands may be used to install Postgrest (see website for more info).
```
wget https://github.com/PostgREST/postgrest/releases/download/v6.0.2/postgrest-v6.0.2-linux-x64-static.tar.xz -O /tmp/postgrest.txz
cd /tmp
tar xf postgrest.txz
chmod +x ./postgrest
sudo mv ./postgrest /usr/local/bin/
```

Postgrest needs a configuration file. A working configuration file is given by
*kwollector-setup-db* output. It looks like:

```
db-uri = "postgres://<db_user>:<db_pass>@<db_host>/<db_name>"
db-schema = "api"
db-anon-role = "kwuser_ro"
jwt-secret = "changemechangemechangemechangemechangeme"
```

(See Postgrest documentation for the options meaning, but no change should be needed).

*kwollector-setup-db* also outputs an *API token* that is needed to perform
write access to the database.

Finally, don't forget to start Postgres with `postgrest
<path_to_configuration_file>`


## Kwollector

The *kwollector* program collects metrics and stores them in the database. It
may run on a any host (provided it can communicate with the database and devices to
monitor).

*kwollector* is available in the kwollect package. Start it with:

```
kwollector <path_to_configuration_file>
```
(a systemd `kwollector.service` file is included in the debian package)


kwollector configuration file should contain:

```
# Path to directory containing metrics description
metrics_dir: /etc/kwollect/metrics.d/

# Hostname of postgresql server
db_host: localhost 

# Database name
db_name: kwdb

# Database user
db_user: kwuser

# Database password
db_password: changeme

# Log level
log_level: warning
```
(option may also be given on the command line, see `kwollector --help`)


### Description of the metrics to fetch

Metrics are described inside yaml files under `<metrics_dir>` directory
(`/etc/kwollect/metrics.d/` by default). For instance, you may have one file per
device containing all metrics to fetch on it.

Here is an example of file content for describing metrics of a device *node-1*:

```
- name: idrac_power_watth_total
  device_id: node-1
  url: snmp://public@node-1-admin.domain.com/1.3.6.1.4.1.674.10892.5.4.600.60.1.7.1.1
  update_every: 5000

- name: idrac_power_watt
  device_id: taurus-1
  url: snmp://public@node-1-admin.domain.com/1.3.6.1.4.1.674.10892.5.4.600.30.1.6.1.3
  update_every: 5000
```

Each metric should be described with:
```
- name:
  device_id:
  url:
  update_every:
  scale_factor:
  labels:
  optional:
```

Where:

- `name` is an unique identifier for this metric (which may be used by several devices)

- `device_id` is an identifier for the device from which the metric is collected

- `url` specifies how and where to get the metric. Currently, SNMP and IPMI protocols are supported.
  - For SNMP, `url` must be in the form `snmp://<community>@<host_address>/<oid>`. For instance:

    `snmp://public@node-1-admin.domain.com/1.3.6.1.4.1.674.10892.5.4.600.30.1.6.1.3`

  - For IPMI, `url` must be in the form
    `ipmisensor://<user>:<password>@<host_address>/<id>`, where *user* and
    *password* are credentials needed to connect to the device using IPMI
    protocol, and *id* is the ID of the sensor to collect (as in the output of
    `ipmi-sensor` command). For instance:

    `url: ipmisensor://root:calvin@node-1-admin.domain.com/20`

    **IPMI protocol needs ipmi-sensor command to be available** (on a Debian
    system, it is available in `freeipmi-tools` package)

  - For Prometheus exporter, `url` must be in the form

    `prometheus://<host_address>:<exporter_port/<filter>`, where *port* is the
    port used by the Prometheus exporter. Optionnally, *filter* may be used to
    indicate which Prometheus metrics to collect. *filter* must
    contain the list of promotheus metrics names separated by "-". For
    instance:

    `url: prometheus://node-1.domain.com:9100/`

    `url: prometheus://node-2.domain.com:9100/node_load1-node_load5-node_load15`


- *Optional* `update_every` specifies the interval between two successive
  fetch for this metric. Default is 10 seconds.

- *Optional* `scale_factor` specifies a scale factor to apply to fetched metric
  value before storing it into the database.

- *Optional* `labels` may be used to record additional information about metric
  being collect (for instance, network interface name). Some labels entries
  have special meaning: `_device_alias` may be used to record an alternative
  name for this metric's device (for instance, if you collect a metric related
  to a port on a network device, you may want to use the device connected to
  this port as a device alias)`

- *Optional* `optional` field must be set to *true* if you don't want this metrics to be
  collected by default (see bellow)



## Graphical interface

TODO


# Advanced topics

## Job scheduler integration

Kwollect may be associated to a [Job
Scheduler](https://en.wikipedia.org/wiki/Job_scheduler) to retrieve metrics
associated to a particular job.

To enable job scheduler integration, it is only needed to fill the
`nodetime_per_job` view in Kwollect's PostgreSQL database. The view should return
SQL data formatted as:

```
+------------+--------------------------+
| Column     | Type                     |
|------------+--------------------------+
| job_id     | integer                  |
| start_time | timestamp with time zone |
| stop_time  | timestamp with time zone |
| node       | text                     |
+------------+--------------------------+
```

Using one line for each *node* (which will be used as *device_id* to retrieve
metrics) involved in the job *job_id* which started at *start_time* and ended
at *end_time* (`NULL` if the job is still running).

We provide such integration for the OAR job scheduler, where
`nodetime_per_job` is automatically filled by querying the OAR database. The
`kwollect-setup-db-oar` tool is available to perform the setup.

With `nodetime_per_job` correctly filled, it becomes possible to perform
requests on `metrics_by_job`, e.g.:

```
SELECT timestamp, device_id, metric_id, value FROM metrics_by_job WHERE job_id = 1234;
```

It is also possible to provide the "job_id" argument when calling API:

```
curl http://kwollect.host:3000/rpc/get_metrics?job_id=1234
```


## Optional metrics

Kwollect handles collecting some metrics "on-demand", for instance for metrics
that don't need to be collected anytime.

These metrics must be configured in kwollector using the *optional: true*
parameter.

Such optional metric will only be collected for a particular device by the
kwollector if the corresponding (*device_id*, *metric_id*) is present in the
`promoted_metrics` table of the Kwollect database (*metric_id* can be a regular
expression to match several metrics at once). This table can be filled
according to specific needs.

For instance, when Kwollect is integrated with OAR job scheduler (see above),
all optional metrics will be enabled for nodes belonging to jobs having
'monitor' type ('monitor=<regexp>' can be used to only capture a subset of
optional metrics). An API endpoint is also created (POST to
`rpc/update_promoted_metrics`), to update `promoted_metrics` table according to
currently existing jobs. It is called by OAR at the beginning and at the end of
the jobs.


## Wattmetre

A specific kwollector, called *kwollector-wattmetre*, is available to read and
store values from OmegaWatt wattmetre. It simply reads [output of OmegaWatt
wattmetre reading program](https://gitlab.inria.fr/delamare/wattmetre-read) and
stores values in the database. For instance in can be invoked with:

```
wattmetre-read /dev/ttyUSB0 42 20 | kwollector-wattmetre <path_to_configuration_file>
```

kwollector-wattmetre configuration file should contain:

```
# Wattmetre identifier, used as 'device_id'
wattmetre_id: wattmetre

# Path to optional wattmetre mapping file, see below
mapping_file_path: ''

# Credentials for DB connection, see kwollector documentation above
db_name: kwdb
db_user: kwuser
db_password: changeme
db_host: localhost

# Log level
log_level: warning
```
(option may also be given on the command line, see `kwollector-wattmetre --help`)

A wattmetre mapping file, describing devices connected to each port of the
wattmetre, may be provided to associate metrics collected from a wattmetre port
to the corresponding device. The file should contain one `device_id:
[wattmetre_id-portX, wattmetre_id-portY]` line per device, containing the
device identifier followed by the list of wattmetres and ports which power it.
