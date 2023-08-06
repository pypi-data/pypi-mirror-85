
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

import csv
import json
from datetime import datetime
import requests


class Sdk:
    '''ReMAP SDK for RUL Algorithms'''

    DIR_BASE = '/app/'
    DATASET_FILE = 'dataset.csv'
    SLOTS_FILE = 'slots.csv'
    WORKFORCE_FILE = 'workforce.csv'
    MATRIX_FILE = 'matrix.csv'
    TASKS_FILE = 'tasks.csv'
    WORKPACKAGES_FILE = 'workpackages.csv'
    AIRCRAFT_TYPE_FILE = 'aircraft_type.csv'
    SKILLS_FILE = 'skills.csv'
    METADATA_FILE = 'metadata.json'
    CONFIG_FILE = 'sdk_config.json'
    METADATA = 'metadata'

    config = None
    start_date = None
    end_date = None
    tailNumber = None
    metadata = None
    aircraft = None
    fleet = None

    def __init__(self):
        '''SDK constructor'''
        with open(self.DIR_BASE+self.CONFIG_FILE) as File:
            self.config = json.load(File)

    def getStartTime(self):
        '''get the start time of metadata'''
        if self.start_date is None:
            with open(self.DIR_BASE+self.METADATA_FILE) as file:
                self.metadata = json.load(file)
            self.start_date = self.metadata['startTime']
        else:
            pass
        return self.start_date

    def getEndTime(self):
        '''get the end time of metadata'''
        if self.end_date is None:
            with open(self.DIR_BASE+self.METADATA_FILE) as file:
                self.metadata = json.load(file)
            self.end_date = self.metadata['endTime']
        else:
            pass
        return self.end_date

    def getTailNumber(self):
        if self.tailNumber is None:
            if self.metadata is None:
                with open(self.DIR_BASE+self.METADATA_FILE) as file:
                    self.metadata = json.load(file)
            self.tailNumber = self.metadata['tailNumber']
        else:
            pass
        return self.tailNumber

    def getAircraft(self):
        ''' get the aircraft '''
        if self.aircraft is None:
            if self.metadata is None:
                with open(self.DIR_BASE+self.METADATA_FILE) as file:
                    self.metadata = json.load(file)
            self.aircraft = self.metadata['aircraft']
        else:
            pass
        return self.aircraft

    def getFleet(self):
        ''' get the fleet '''
        if self.fleet is None:
            if self.metadata is None:
                with open(self.DIR_BASE+self.METADATA_FILE) as file:
                    self.metadata = json.load(file)
            self.fleet = self.metadata['fleet']
        else:
            pass
        return self.fleet

    def getMetadata(self):
        with open(self.DIR_BASE+self.METADATA_FILE) as file:
            self.metadata = json.load(file)
        return self.metadata['metadata']

    def getReplacements(self):
        if self.metadata is None:
            with open(self.DIR_BASE+self.METADATA_FILE) as file:
                self.metadata = json.load(file)
        return self.metadata['replacements']

    def getDataset(self):
        return self.DIR_BASE+self.DATASET_FILE

    def getSlots(self):
        return self.DIR_BASE+self.SLOTS_FILE

    def getWorkforce(self):
        return self.DIR_BASE+self.WORKFORCE_FILE

    def getMatrix(self):
        return self.DIR_BASE+self.MATRIX_FILE

    def getTasks(self):
        return self.DIR_BASE+self.TASKS_FILE

    def getWorkpackages(self):
        return self.DIR_BASE+self.WORKPACKAGES_FILE

    def getAircraftType(self):
        return self.DIR_BASE+self.AIRCRAFT_TYPE_FILE

    def getSkills(self):
        return self.DIR_BASE+self.SKILLS_FILE

    # return the component PartNo of the parameter passed as param
    def getParamPartNumber(self, param):
        PartNo = "P/N Not Found"
        if self.metadata is None:
            with open(self.DIR_BASE+self.METADATA_FILE) as file:
                self.metadata = json.load(file)
        self.metadata = self.metadata[self.METADATA]
        for x in self.metadata:
            if x.__contains__('parameter'):
                parameter = x['parameter']
                if parameter is not None:
                    name = parameter['name']
                    if name == param:
                        component = parameter['component']
                        PartNo = component['partNo']
        return PartNo

    def sendOutput(self, jsonoutput):
        secret = self.__getClientSecret()
        payload = jsonoutput
        payload['serial'] = self.config['serial']
        payload['dataset'] = self.config['dataset']
        payload['model'] = self.config['model']
        payload['status'] = "FINISHED"
        payload['runnerId'] = self.config['runnerId']

        token = self.__getKCToken(secret)
        json_dump = json.dumps(payload)
        headers = {"Content-Type": "application/json",
                   "Authorization": "Bearer "+token}
        r = requests.post(self.config['OUTPUT_URL'],
                          headers=headers, data=json_dump)
        return (r.text)

    def sendScheduleOutput(self, schedule_file):
        secret = self.__getClientSecret()
        token = self.__getKCToken(secret)
        headers = {"Content-Type": "application/json",
                   "Authorization": "Bearer "+token}

        with open(schedule_file, 'rb') as f:
            r = requests.post(self.config['SCHEDULE_OUTPUT_URL'],
                              headers=headers, files={'output.xls': f})
        return (r.text)

    def __getKCToken(self, secret):

        url = self.config['KC_TOKEN_URL']
        payload = {
            "client_id": self.config['CLIENT_ID'],
            "grant_type": "client_credentials",
            "client_secret": secret}
        r = requests.post(url, data=payload)
        res = json.loads(r.text)
        return (res['access_token'])

    def __getClientSecret(self):

        secret = "Secret Not Found"
        with open(self.DIR_BASE+'secret') as file:
            secret = file.read()
        return secret
