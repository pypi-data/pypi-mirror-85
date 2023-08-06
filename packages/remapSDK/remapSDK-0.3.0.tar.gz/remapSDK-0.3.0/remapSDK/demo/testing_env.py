
'''
   Copyright © 2019  Atos Spain SA. All rights reserved.
  
   This file is part of the ReMAP platform.
  
   The ReMAP platform is free software: you can redistribute it 
   and/or modify it under the terms of GNU GPL v3.
   
   THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT ANY WARRANTY OF ANY KIND, 
   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
   MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT, 
   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
   CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN ACTION OF CONTRACT, TORT 
   OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
   OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
   See README file for the full disclaimer information and LICENSE file 
   for full license information in the project root.  
  '''
from flask import Flask, json, request 
import os
import csv
from shutil import copyfile

print("ReMAP SDK Testing Environment")

DATA_DIR='/app/'

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

copyfile("./data/dataset.csv", "/app/dataset.csv")
copyfile("./data/tasks.csv", "/app/tasks.csv")
copyfile("./data/schedule.csv", "/app/schedule.csv")
copyfile("./data/metadata.json", "/app/metadata.json")
copyfile("./data/sdk_config.json", "/app/sdk_config.json")
copyfile("./data/secret", "/app/secret")

print("configuration loaded")
#-------------------------------------

api = Flask(__name__)

@api.route('/mock/getToken', methods=['POST'])
def getToken():
  req_data = {"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJSZU1BUCBNb2NrIEF1dGggU2VydmVyIiwiaWF0IjoxNTk3MTQ0MjkzLCJleHAiOjE2Mjg2ODAyOTMsImF1ZCI6IlRlc3RpbmdfU0RLIiwic3ViIjoidGVzdGluZ19zZGtAcmVtYXAuZXUiLCJHaXZlbk5hbWUiOiJBbGV4IiwiU3VybmFtZSI6IkdhcmNpYSIsIkVtYWlsIjoiYWxlamFuZHJvLmdhcmNpYUBhdG9zLm5ldCIsIlJvbGUiOlsiU29mdHdhcmUgZW5naW5lZXIiLCJQcm9qZWN0IEFkbWluaXN0cmF0b3IiLCJSZXNlYXJjaGVyIl19.sJBKiT1gOkaXKliiWXFF2jKH_aqGf_AHS27wZwkcsoM"}
  return req_data

@api.route('/mock/output', methods=['POST'])
def post_output():
  print("SDK Output received")

  req_data = request.get_json()
  print(req_data)
  return json.dumps(req_data)

@api.route('/mock/scheduleOutput', methods=['POST'])
def post_schedule_output():
  print("SDK Output received")
  return json.dumps('ok')

if __name__ == '__main__':
    print("Mock ReMAP server for SDK Testing")
    api.run()