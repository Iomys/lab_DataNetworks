"""
Script to test the REST API
author : Valentin Sandoz, valentin.sandoz@students.hevs.ch
date : 30.01.2023
"""
import requests
import json
import time

server = "blackpi009.hevs.ch"
# server = "127.0.0.1"

open_data = {"value": "open"}
object_dumped = json.dumps(open_data)
r = requests.post(f'http://{server}:8080/plugs/my_strom-009/relay', data=json.dumps(open_data))
print(r)
time.sleep(1)
close_data = {"value": "close"}
r = requests.post(f'http://{server}:8080/plugs/my_strom-009/relay', data=json.dumps(close_data))

print(r)



#%%
