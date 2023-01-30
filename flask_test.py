"""
Script to test the REST API
author : Valentin Sandoz, valentin.sandoz@students.hevs.ch
date : 30.01.2023
"""
import requests
import json
import time


open_data = {"value": "open"}
object_dumped = json.dumps(open_data)
r = requests.post('http://127.0.0.1:8080/plugs/my_strom-009/relay', data=json.dumps(open_data))
time.sleep(1)
close_data = {"value": "close_data"}
r = requests.post('http://127.0.0.1:8080/plugs/my_strom-009/relay', data=json.dumps(close_data))

print(r)
