# TheHive webhooks

TheHive can notify external system of modification events (case creation, alert update, task assignment, ...).

## Define webhook endpoints
In application.conf add the following section:
```
notification.webhook.endpoints = [
  {
    name: local
    url: "http://127.0.0.1:5000/"
    version: 0
    wsConfig: {}
    includedTheHiveOrganisations: ["*"]
    excludedTheHiveOrganisations: []
  }
]
```

The `name` is the identifier of the endpoint. It is used when the webhook is setup for an organisation.
The `version` defines the format of the message. If `version` is `0`, TheHive will send messages with the same format as TheHive3. Currently TheHive only supports version 0.
The setting `wsConfig` is the configuration of HTTP client. It contains proxy, SSL and timeout configuration.
`includedTheHiveOrganisations` and `excludedTheHiveOrganisations` defines which organisations can use this endpoint. If `includedTheHiveOrganisations` is empty or contains `*`, all organisation is accepted, except those which are in `excludedTheHiveOrganisations`.

## Activate webhooks
This action must be done by an organisation admin (with permission manageConfig) and requires to run a curl command:
```
read -p 'Enter the URL of TheHive: ' thehive_url
read -p 'Enter your login: ' thehive_user
read -s -p 'Enter your password: ' thehive_password

curl -XPUT -u$thehive_user:$thehive_password -H 'Content-type: application/json' $thehive_url/api/config/organisation/notification -d '
{
  "value": [
    {
      "delegate": false,
      "trigger": { "name": "AnyEvent"},
      "notifier": { "name": "webhook", "endpoint": "local" }
    }
  ]
}'
```
