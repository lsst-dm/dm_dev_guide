#################################################
Service Integration with the LDF Monitoring Stack
#################################################

Premise
=======

As services are implemented in the LDF environment, the LDF monitoring stack will
need a way to ask these services about their health and performance related metrics
in order to detect issues with the service and to gather data in regards to reporting.
The methods used to expose this data need to conform to a set of standards that are
compatible with the capabilities of the LDF monitoring framework.
A draft of acceptable methods is outlined below.

Method 1: Direct Injection to InfluxDB Endpoint
===============================================
Streaming metrics straight into an InfluxDB database is an efficient way
to inject data into the LDF monitoring framework.
The `documentation for writing data into InfluxDB`_ is well define and very conventional.
NCSA admins working on monitoring are also happy to answer questions about this method
and when it comes time for final integration will be available to provision databases
and ensure that metrics data is flowing properly into InfluxDB as well as create
relevant dashboards for those services.  

.. _documentation for writing data into InfluxDB: https://docs.influxdata.com/influxdb/v1.5/guides/writing_data/

Method 2: Telegraf
==================
Certain applications have built in support via the `Telegraf agent`_ which
make deploying monitoring of a service fairly straight forward.
One will have to include the telegraf package in the container image with
a proper output section format. See the :ref:`example <example01>` below.

.. _Telegraf agent: https://github.com/influxdata/telegraf/tree/master/plugins/inputs

Method 3: Prometheus Endpoint 
=============================
Another option though sometimes less preferred due to a bit high memory
footprint is to configure a Prometheus endpoint for the application that
can be scraped by the LDF monitoring system.
Many applications already have integrations with `Prometheus`_.
If an integration is not provided there is documentation on writing a `custom integration`_.

.. _Prometheus: https://prometheus.io/docs/instrumenting/exporters/
.. _custom integration: https://prometheus.io/docs/instrumenting/writing_exporters/

.. _example01
Example: Telegraf Output Configuration
======================================

[[outputs.influxdb]]
  database = "$database_name"
  urls = ["https://$influxhostname:8086"]

