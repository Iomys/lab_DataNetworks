#!/usr/bin/env python3
"""
The script measures the power and the temperature from the plug and pushes them on the MQTT broker.
The script reads the @set topic and shut on/off the plug's relays on commands

author : Valentin Sandoz, valentin.sandoz@students.hevs.ch
date : 30.01.2023
"""
import tomli
import json
import logging
import time
from plug import MyStromSwitch
import paho.mqtt.client as mqtt

# Import credentials and configuration
with open("credentials.toml", "rb") as f:
    toml_dict = tomli.load(f)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MyStrom Switch object
my_switch = MyStromSwitch(name=toml_dict["MyStromSwitch"]["name"], macAddress=toml_dict["MyStromSwitch"]["macAdress"])

#MQTT parameters
mqtt_path_set = f"@set/{my_switch.name}/control/#"
#mqtt_path_update = f"@set/{my_switch.name}/control/#"
mqtt_broker = toml_dict["MQTT"]["broker"]
mqtt_username = toml_dict["MQTT"]["username"]
mqtt_password = toml_dict["MQTT"]["password"]

# Init paho MQTT
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(mqtt_path_set)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    decode_MQTT(payload)

def decode_MQTT(payload):
    try:
        payload_dict = json.loads(payload)
        if payload_dict["value"] == "open":
            my_switch.setState(False)
        elif payload_dict["value"] == "close":
            my_switch.setState(True)
    except json.decoder.JSONDecodeError as e:
        logging.warning(e)
        logging.warning("Erreur de décodage JSON")
    except KeyError:
        logging.debug("KeyError : Mauvaise input MQTT probablement")
        # Ne fais rien s'il n'y a pas la clé "valeur" dans le json
        pass


client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()
# Take the measures

def publish_temp(switch=my_switch):
    topic = f"@update/{switch.name}/monitoring/temperature"
    dict_to_publish = {
        "value": switch.getTemp(),
        "unit" : "C"
    }
    payload = json.dumps(dict_to_publish)
    client.publish(topic, payload)


def publish_power(switch=my_switch):
    topic = f"@update/{switch.name}/monitoring/power"
    dict_to_publish = {
        "value": switch.getPower(),
        "unit" : "W"
    }
    payload = json.dumps(dict_to_publish)
    client.publish(topic, payload)

while 1:
    publish_temp(my_switch)
    publish_power(my_switch)
    time.sleep(1)




