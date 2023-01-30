from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, WriteOptions


class DbConnector:
    """
    Connector to the influx db
    """
    def __init__(self, token, org, bucket):
        self.client = InfluxDBClient(url="https://influx.sdi.hevs.ch", token=token, org=org)
        self.org = org
        self.bucket = bucket

        # Options to write measures in batch
        options = WriteOptions(
            batch_size=500,  # every 500 measure or
            flush_interval=10_000,  # every 10 seconds
            jitter_interval=2_000,  # +- 2 second
            retry_interval=5_000,
            max_retries=5,          # retry max 5 times if connection problem
            max_retry_delay=30_000,
            exponential_base=2
        )
        self.influx_writer = self.client.write_api(write_options=WriteOptions(options))

    def publish_measurement(self, measurement, value, switch, unit):
        if type(value) == int:
            value = float(value)
        point = Point(measurement) \
            .field(measurement, value) \
            .tag("unit", unit) \
            .tag("switch", switch) \
            .time(datetime.utcnow())

        self.influx_writer.write(self.bucket, self.org, point)
