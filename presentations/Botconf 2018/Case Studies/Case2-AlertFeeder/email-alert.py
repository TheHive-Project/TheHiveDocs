#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import requests
import sys
import json
import time
import uuid
from thehive4py.api import TheHiveApi
from thehive4py.models import Alert, AlertArtifact

api = TheHiveApi('http://<PUT_THEHIVE_URL_HERE>','<PUT_API_KEY_FOR_AUTHENTICATION_HERE>', None, {'http': '', 'https': ''})

# Uncomment lines, add new ones as you need to below.
# WARNING: if you submit files with the alert, they need to be in the same directory as this code.
artifacts = [
    #AlertArtifact(dataType='file', data='sample.txt',tags=['attachment'])
    #AlertArtifact(dataType='url',data='xxx',tags=['suspicious-url']),
    #AlertArtifact(dataType='domain',data='xxx',tags=['suspicious-domain']),
    #AlertArtifact(dataType='mail',data='xxx',tags=['sender']),
    #AlertArtifact(dataType='mail_subject',data='some subject)
]


# Prepare the sample Alert
sourceRef = str(uuid.uuid4())[0:6]
alert = Alert(title='<CUSTOMIZE THE TITLE>',
              tlp=2,
              tags=['<add tag here>'],
              description='<add some description>',
              type='notification',
              source='Email Server',
              sourceRef=sourceRef,
              artifacts=artifacts)

# Create the Alert
print('Create Alert')
print('-----------------------------')
id = None
response = api.create_alert(alert)
if response.status_code == 201:
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    print('')
    id = response.json()['id']
else:
    print('ko: {}/{}'.format(response.status_code, response.text))
    sys.exit(0)


# Get all the details of the created alert
print('Get created alert {}'.format(id))
print('-----------------------------')
response = api.get_alert(id)
if response.status_code == requests.codes.ok:
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    print('')
else:
    print('ko: {}/{}'.format(response.status_code, response.text))
