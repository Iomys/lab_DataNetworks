#!/usr/bin/env python3
"""
This script gets the monitoring measurements from MQTT and pushes the on the influx db
"""

import paho.mqtt.client as mqtt
import json
from pathlib import Path
import tomli
from influx import DbConnector

# Import credentials
with open("credentials.toml", "rb") as f:
    toml_dict = tomli.load(f)


# Influx variables
token = toml_dict["InfluxDB"]["token"]
org = toml_dict["InfluxDB"]["org"]
bucket = toml_dict["InfluxDB"]["bucket"]

influx_client = DbConnector(token, org, bucket)

# MQTT variables
mqtt_path_update = f"@update/+/monitoring/#"
mqtt_broker = toml_dict["MQTT"]["broker"]
mqtt_username = toml_dict["MQTT"]["username"]
mqtt_password = toml_dict["MQTT"]["password"]



def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(mqtt_path_update)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    topic = msg.topic.split("/")
    if topic[0] == "@update":
        if topic[2] == "monitoring":
            try:
                payload = json.loads(payload)
                influx_client.publish_measurement(measurement=topic[3], value=payload["value"], switch=topic[1], unit=payload["unit"])
            except json.decoder.JSONDecodeError:
                pass


# Initialisation of MQTT client
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(mqtt_username, mqtt_password)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(mqtt_broker, 1883, 60)
mqtt_client.loop_forever()

