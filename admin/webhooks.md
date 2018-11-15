# WebHooks

Starting from version 2.13, TheHive supports [webhooks](https://en.wikipedia.org/wiki/Webhook). When enabled, TheHive will send each action that has been performed on it (add case, update case, add task, ...), in real time, to an HTTP endpoint. You can then create a program or application on the HTTP endpoint to react on specific events.

  * [Configuration](#configuration)
  * [Data Sent to the HTTP Endpoint](#data-sent-to-the-http-endpoint)
  * [Sample Webhook Server Application](#sample-webhook-server-application)
    * [Dependencies](#dependencies)
    * [Python Script](#python-script)
    * [Run](#run)

## Configuration
Webhooks are configured using the `webhook` key in the configuration file (`/etc/thehive/application.conf` by default). A minimal configuration contains an arbitrary name and an URL. The URL corresponds to the HTTP endpoint:
```
webhooks {
  myLocalWebHook {
    url = "http://my_HTTP_endpoint/webhook"
  }
}
```

[Proxy and SSL configuration can be added](configuration.md#8-http-client-configuration) in the same manner as for MISP or Cortex:

```
webhooks {
  securedWebHook {
    url = "https://my_HTTP_endpoint/webhook"
    ws {
      ssl.trustManager {
        stores = [
          {
            type: "JKS" // JKS or PEM
            path: "keystore.jks"
            password: "password1"
          }
        ]
      }
      proxy {
        host: "10.1.0.1"
        port: 3128
      }
    }
  }
}
```

## Data Sent to the HTTP Endpoint
For each action performed on it, TheHive sends an audit trail entry in JSON format to the HTTP endpoint. Here is an example corresponding to the creation of a case:

```
{
  "operation": "Creation",                                        # Creation, Update or Delete
  "objectType": "case",                                           # Type of object
  "objectId": "AV6FZsTj0KeanEfOQfd_",                             # Object ID
  "startDate": 1505476659427,                                     # When the operation has been done
  "requestId": "13b17ff13d1cfc56:2b7b048b:15e84f42c33:-8000:426", # HTTP request ID which has done the operation
  "details": {                                                    # Attributes used for creation of update
    "customFields": {},
    "metrics": {},
    "description": "Example of case creation",
    "flag": false,
    "title": "Test case for webhook",
    "status": "Open",
    "owner": "me",
    "caseId": 1445,
    "severity": 2,
    "tlp": 2,
    "startDate": 1505476620000,
    "tags": []
  },
  "base": true,                                                   # Internal information used to determine the main operation when there are several operations for the same request
  "rootId": "AV6FZsTj0KeanEfOQfd_",                               # ID of the root parent of the object (internal use)
  "object": {                                                     # The object after the operation
    "customFields": {},
    "metrics": {},
    "createdBy": "me",
    "description": "Example of case creation",
    "flag": false,
    "user": "me",
    "title": "Test case for webhook",
    "status": "Open",
    "owner": "me",
    "createdAt": 1505476658289,
    "caseId": 1445,
    "severity": 2,
    "tlp": 2,
    "startDate": 1505476620000,
    "tags": [],
    "id": "AV6FZsTj0KeanEfOQfd_",
    "_type": "case"
  }
}
```

For an update, the data will look like:
```
{
  "operation": "Update",
  "details": {
    "severity": 3
  },
  "objectType": "case",
  "objectId": "AV6FZsTj0KeanEfOQfd_",
  "base": true,
  "startDate": 1505477372601,
  "rootId": "AV6FZsTj0KeanEfOQfd_",
  "requestId": "13b17ff13d1cfc56:2b7b048b:15e84f42c33:-8000:446",
  "object": {
    "customFields": {},
    "metrics": {},
    "createdBy": "me",
    "description": "Example of case creation",
    "flag": false,
    "user": "me",
    "title": "Test case for webhook",
    "status": "Open",
    "owner": "me",
    "createdAt": 1505476658289,
    "caseId": 1445,
    "severity": 3,
    "tlp": 2,
    "startDate": 1505476620000,
    "tags": [],
    "updatedBy": "me",
    "updatedAt": 1505477372246,
    "id": "AV6FZsTj0KeanEfOQfd_",
    "_type": "case"
  }
}
```

## Sample Webhook Server Application
The following application is a sample intended to help you get started with webhooks. It is very basic as it listens to a local port and displays the contents of the received POST JSON data.

### Dependencies
Install dependencies:
`sudo pip install flask`

### Python Script
Create a simple Python script (e.g. `webhooktest.py`):

```
from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/',methods=['POST'])
def foo():
   data = json.loads(request.data)
   print(json.dumps(data, indent=4))
   return "OK"

if __name__ == '__main__':
   app.run()

```
### Run
Run the server:
`python webhooktest.py`
