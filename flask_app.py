"""
Flask server running a REST API to update the my_strom-switch relay
author : Valentin Sandoz, valentin.sandoz@students.hevs.ch
date : 30.01.2023
"""
import re

from flask import Flask, request, Response
import json
import paho.mqtt.client as mqtt
import tomli
app = Flask(__name__)

# Import credentials
with open("credentials.toml", "rb") as f:
    toml_dict = tomli.load(f)

# MQTT variables
mqtt_broker = toml_dict["MQTT"]["broker"]
mqtt_username = toml_dict["MQTT"]["username"]
mqtt_password = toml_dict["MQTT"]["password"]

# Init MQTT client
client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.connect(mqtt_broker, 1883, 60)



@app.route('/')
def index():
    return 'Server Works!'


@app.route('/plugs/<plug>/relay', methods=['POST'])
def post_plug_relay(plug):
    """
    method to make plug API
    :param plug: name of the plug, must be my_strom-xxx
    :return: Json response
    """
    #global client
    # Vérification que ce soit bien un format de plus qui puisse exister
    if not re.match(r"my_strom-[0-9]{3}", plug):
        return "404 Plug not found", 404, {'ContentType': 'text/plain'}
    try:
        user_input = json.loads(request.data.decode())
        topic = f"@set/{plug}/control/relay"
        if user_input["value"] == "open":
            print(f"Plug {plug} is opened")
            client.publish(topic=topic, payload=json.dumps({"value": "open"}))
        elif user_input["value"] == "close":
            print(f"Plug {plug} is closed")
            client.publish(topic=topic, payload=json.dumps({"value": "close"}))
        else:
            return "400 Bad Request, value takes 'open' or 'close'", 400, {"ContentType": "text/plain"}
    except KeyError:
        return "400 Bad Request, value does not exist", 400, {"ContentType": "text/plain"}
    except json.JSONDecodeError:
        return "400 Bad Request : Not JSON", 400, {"ContentType": "text/plain"}

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == "__main__":
    app.run(host='blackpi009.hevs.ch', port=8080, ssl_context=('cert.pem', 'key.pem'))
