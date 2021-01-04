# TheHive Connectors



## Cortex

The Cortex connector module needs to be enabled to allow TheHive work with Cortex.
TheHive is able to connect more than one Cortex server.

Several parameters can be configured for one server :

- **name**: name given to the Cortex instance (eg: _Cortex-Internal_)
- **url**: url to connect to the Cortex instance
- **auth**: method used to authenticate on the server (_bearer_ if using API keys)
- **wsConfig**: network configuration dedicated to Play Framework for SSL and proxy
- **refreshDelay**: frequency of job updates checks (default: 5 seconds)
- **maxRetryOnError**: maximum number of successive errors before give up (default: _3_)
- **statusCheckInterval**: check remote Cortex status time interval (default: _1 minute_)
- **includedTheHiveOrganisations**: list of TheHive organisations which can use this Cortex server (default: _all ("\*")_ )
- **excludedTheHiveOrganisations**: list of TheHive organisations which cannot use this Cortex server (default: _None_ )

**Note**: By default, adding a Cortex server in TheHive configuration make it available for all organisations added on the instance.

This configuration has to be added to TheHive `conf/application.conf` file:

```yaml
play.modules.enabled += org.thp.thehive.connector.cortex.CortexModule
cortex {
  servers = [
    {
      name = local
      url = "http://localhost:9001"
      auth {
        type = "bearer"
        key = "[REDACTED]"
      }
      # HTTP client configuration (SSL and proxy)
      #  wsConfig {}
     # List TheHive organisation which can use this Cortex server. All ("*") by default
     # includedTheHiveOrganisations = ["*"]
     # List TheHive organisation which cannot use this Cortex server. None by default
     # excludedTheHiveOrganisations = []
    }
  ]
  # Check job update time intervalcortex
  refreshDelay = 5 seconds
  # Maximum number of successive errors before give up
  maxRetryOnError = 3
  # Check remote Cortex status time interval
  statusCheckInterval = 1 minute
}
```



## MISP

The MISP connector module needs to be enabled to allow TheHive to interact with MISP.
TheHive is able to connect to more than one MISP server for pulling, pushing or both.

Several parameters can be configured for one server :

- **interval**: delay between to pull/push events to remote MISP servers. This is a common parameter for all configured server
- **name**: name given to the MISP instance (eg: _MISP-MyOrg_)
- **url**: url to connect to the MISP instance
- **auth**: method used to authenticate on the server (_bearer_ if using API keys)
- **purpose**: define the purpose of the server MISP: ImportOnly, ExportOnly or ImportAndExport (default: ImportAndExport)
- **wsConfig**: network configuration dedicated to Play Framework for SSL and proxy
- **caseTemplate**: case template used by default in TheHive to import events as Alerts
- **tags**: tags to be added to events imported as Alerts in TheHive
- **exportCaseTags**: indicate if the tags of the case should be exported to MISP event (default: false)

Optional parameters can be added to filter out some events coming into TheHive:

- **exclusion.organisations**: list of MISP organisation from which event will not be imported
- **exclusion.tags**: don't import MISP events which have one of these tags
- **whitelist.organisations**: import only events from these MISP organisations
- **whitelist.tags**: import only MISP events which have one of these tags
- **max-age**: maximum age of the last publish date of event to be imported in TheHive 
- **includedTheHiveOrganisations**: list of TheHive organisations which can use this MISP server (default: _all ("\*")_ )
- **excludedTheHiveOrganisations**: list of TheHive organisations which cannot use this MISP server (default: _None_ )

Additionally, some organisations or tags from MISP can be defined to exclude events. 

---
**Note**

By default, adding a MISP server in TheHive configuration make it available for all organisations added on the instance.

---

This configuration has to be added to TheHive `conf/application.conf` file:



```yaml
## MISP configuration
# More information at https://github.com/TheHive-Project/TheHiveDocs/TheHive4/Administration/Connectors.md
# Enable MISP connector
play.modules.enabled += org.thp.thehive.connector.misp.MispModule
misp {
  interval: 1 hour
  servers: [
    {
      name = "local"            # MISP name
      url = "http://localhost/" # URL or MISP
      auth {
        type = key
        key = "***"             # MISP API key
      }
      wsConfig {}                        # HTTP client configuration (SSL and proxy)
      # Name of the case template in TheHive that shall be used to import
      # MISP events as cases by default.
      #caseTemplate = "<Template_Name_goes_here>"
      #
      # Optional tags to add to each observable  imported  from  an  event
      # available on this instance.
      #tags = ["misp-server-id"]
      #
      # The age of the last publish date
      #max-age = 7 days
      #
      # Organization and tags 
      # exclusion {
      #  organisation = ["bad organisation", "other orga"]
      #  tags = ["tag1", "tag2"]
      #  }
      # whitelist {
      #   tags = ["tag1", "tag2"]
      # }
    }
  ]
} 
```

