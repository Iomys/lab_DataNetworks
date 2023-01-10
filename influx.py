from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, WriteOptions

# You can generate an API token from the "API Tokens Tab" in the UI
token = "NA34jiwvVvgLnOUzMsIVtvgeVvsXxgapZek526GhfePDktIgp8pnXzmKuhn8LYfvOSgymbzce57g12wSVNUbeQ=="
org = "SIn09"
bucket = "SIn09"


# with InfluxDBClient(url="https://influx.sdi.hevs.ch", token=token, org=org) as mqtt_client:
#     point = Point("mem") \
#         .tag("host", "host1") \
#         .field("used_percent", 23.43234543) \
#         .time(datetime.utcnow(), WritePrecision.NS)
#
#     mqtt_client.write(bucket, org, point)


class DbConnector:

    def __init__(self, token, org, bucket):
        self.client = InfluxDBClient(url="https://influx.sdi.hevs.ch", token=token, org=org)
        self.org = org
        self.bucket = bucket

        options = WriteOptions(
            batch_size=500,
            flush_interval=10_000,
            jitter_interval=2_000,
            retry_interval=5_000,
            max_retries=5,
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



