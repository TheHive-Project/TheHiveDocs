# TheHive Installation Using Docker

This guide assumes that you will use [Docker](https://www.docker.com/).

## How to Use the Docker Image

Starting from version 2.11 (Mellifera), TheHive Docker image doesn't come with ElasticSearch. As TheHive requires it to work, you can:
 - use docker-compose
 - manually install and configure ElasticSearch.

### Use Docker-compose

Docker-compose can start multiple dockers and link them together. It can be installed using the
[documentation](https://docs.docker.com/compose/install/).
The following [docker-compose.yml](https://raw.githubusercontent.com/TheHive-Project/TheHive/master/docker/thehive/docker-compose.yml)
file starts ElasticSearch, Cortex and TheHive:
```
version: "2"
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:5.5.2
    environment:
    	- http.host=0.0.0.0
    	- transport.host=0.0.0.0
    	- xpack.security.enabled=false
    	- cluster.name=hive
      - script.inline=true
      - thread_pool.index.queue_size=100000
      - thread_pool.search.queue_size=100000
      - thread_pool.bulk.queue_size=100000
  cortex:
    image: certbdf/cortex:latest
    ports:
      - "0.0.0.0:9001:9000"
  thehive:
    image: certbdf/thehive:latest
    depends_on:
      - elasticsearch
      - cortex
    ports:
      - "0.0.0.0:9000:9000"
```
Put this file in an empty folder and run `docker-compose up`. TheHive is exposed on 9000/tcp port and Cortex on
9001/tcp. These ports can be changed by modifying the `docker-compose` file.

You can specify a custom `application.conf` file by adding the lines, in `thehive` section:
```
volumes:
    - /path/to/application.conf:/etc/thehive/application.conf
```

You should define where the data (i.e. the ElasticSearch database) will be stored in your server by adding the lines, in `elasticsearch` section:
```
volumes:
    - /path/to/data:/usr/share/elasticsearch/data
```


### Manual Installation of ElasticSearch

ElasticSearch can be installed on the same server as TheHive or on a different one. You can then configure TheHive according to the
[documentation](../admin/configuration.md) and run TheHive docker as follow:
```
docker run --volume /path/to/thehive/application.conf:/etc/thehive/application.conf certbdf/thehive:latest --no-config
```

You can add the `--publish` docker option to expose TheHive HTTP service.

## Customize the Docker Image

By Default, TheHive docker image adds minimal configuration:
 - choose a random secret (play.crypto.secret)
 - search ElasticSearch instance (host named `elasticsearch`) and add it to configuration
 - search Cortex instance (host named `cortex`) and add it to configuration

This behavior can be disabled by adding `--no-config` to the docker command line:
`docker run certbdf/thehive:latest --no-config` or by adding the line `command: --no-config` in `thehive` section of
docker-compose file.

The image accepts more options:
 - --no-config             : do not try to configure TheHive (add secret and elasticsearch)
 - --no-config-secret      : do not add random secret to configuration
 - --no-config-es          : do not add elasticsearch hosts to configuration
 - --es-hosts <esconfig>   : use this string to configure elasticsearch hosts (format: ["host1:9300","host2:9300"])
 - --es-hostname <host>    : resolve this hostname to find elasticseach instances
 - --secret <secret>       : secret to secure sessions
 - --cortex-proto <proto>  : define protocol to connect to Cortex (default: http)
 - --cortex-port <port>    : define port to connect to Cortex (default: 9000)
 - --cortex-url <url>      : add Cortex connection
 - --cortex-hostname <host>: resolve this hostname to find Cortex instances


Please remember that you must install and configure ElasticSearch.

## How to Use The Docker Image

Once you have installed and configured ElasticSearch as shown above, the easiest way to start Cortex is the following one:
```
docker run certbdf/thehive
```
