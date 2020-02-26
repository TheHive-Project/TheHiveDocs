# TheHive Connectors



## Cortex

The Cortex connector module needs to be enabled to allow TheHive work with Cortex.
TheHive is able to connect more than one Cortex server.

several parameters can be configured for one server :

- **name**: name given to the Cortex instance (eg: _Cortex-Internal_)
- **url**: url to connect to the Cortex instance
- **auth**: method used to authenticate on the server (_bearer_ if using API keys)
- **wsConfig**: network configuration dedicated to Play Framework for SSL and proxy
- **refreshDelay**: frequency of job updates checks (default: _1 minute_)
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
      # Check job update time intervalcortex
      refreshDelay = 1 minute
      # Maximum number of successive errors before give up
      maxRetryOnError = 3
      # Check remote Cortex status time interval
      statusCheckInterval = 1 minute
      # List TheHive organisation which can use this Cortex server. All ("*") by default
      # includedTheHiveOrganisations = ["*"]
      # List TheHive organisation which cannot use this Cortex server. None by default
      # excludedTheHiveOrganisations = []
    }
  ]
}
```



## MISP

