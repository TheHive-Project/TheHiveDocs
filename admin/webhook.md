# WebHooks

From TheHive 2.13, you can configure webhooks. In this case, each action done on
TheHive platform (update a case, add a task, ...) is sent to an http endpoint.
You can then create a tool that listen on http port and act when specific event
occurs.

## Configuration

Webhooks are configured under `webhook` key in configuration. Minimal
configuration must contain an arbitrary name and an url:
```
webhooks {
  myLocalWebHook {
    url = "http://localhost:8000/webhook"
  }
}
```

Proxy and SSL configuration can be added in the same manner than MISP or Cortex
(cf. [configuration guide, section 8. HTTP client configuration](configuration.md#8-http-client-configuration):

```
webhooks {
  securedWebHook {
    url = "https://remoteSSLWebHook.com/webhook"
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

## Data sent to Webhook

TheHive sent audit trail to webhook. Here is an example of case creation:
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

For an update, data looks like:
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
## Sample Webhook server application
This application might help you to get started with webhooks.
It listens to a local port and displays the contents of received POST json data.

Install dependencies:
`sudo pip install flask`

Create a simple Python script (e.g. `vi webhooktest.py`):
```
from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/',methods=['POST'])
def foo():
   data = json.loads(request.data)
   print json.dumps(data, indent=4)
   return "OK"

if __name__ == '__main__':
   app.run()

```

Run the server:
`python webhooktest.py`
