"""
Flask server running a REST API to update the my_strom-switch relay
author : Valentin Sandoz, valentin.sandoz@students.hevs.ch
date : 30.01.2023
"""
import re # regex
from flask import Flask, request
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
    # global client # Ne fonctionne pas avec le mot clef global, mais sans oui
    # Vérification que ce soit bien un format de fiche qui puisse exister
    if not re.match(r"my_strom-[0-9]{3}", plug):
        return "404 Plug not found", 404, {'ContentType': 'text/plain'}
    try:
        user_input = json.loads(request.data.decode())  # decode JSON
        topic = f"@set/{plug}/control/relay"            # topic to send the command
        if user_input["value"] == "open":
            print(f"Plug {plug} is opened")
            client.publish(topic=topic, payload=json.dumps({"value": "open"}))
        elif user_input["value"] == "close":
            print(f"Plug {plug} is closed")
            client.publish(topic=topic, payload=json.dumps({"value": "close"}))
        else:
            return "400 Bad Request, value takes 'open' or 'close'", 400, {"ContentType": "text/plain"}
    except KeyError:  # if the dict has not the key 'value'
        return "400 Bad Request, value does not exist", 400, {"ContentType": "text/plain"}
    except json.JSONDecodeError:  # if this is not JSON
        return "400 Bad Request : Not JSON", 400, {"ContentType": "text/plain"}

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == "__main__":
    # Ne fonctionne pas en https car l certificat n'est pas valide => requests refuse
    app.run(host='blackpi009.hevs.ch', port=8080)
