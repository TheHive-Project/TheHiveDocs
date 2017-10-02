# Installation guide of ElasticSearch

ElasticSearch can be installed using system package or docker. The latter is preferred as its installation and update
are easier.

## Install ElasticSearch using system package
Install the ElasticSearch package provided by Elastic:
```
# PGP key installation
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key D88E42B4

# Alternative PGP key installation
# wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -

# Debian repository configuration
echo "deb https://artifacts.elastic.co/packages/5.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-5.x.list

# Install https support for apt
sudo apt install apt-transport-https

# ElasticSearch installation
sudo apt update && sudo apt install elasticsearch
```

The Debian package does not start up the service by default. The reason for this is to prevent the instance from
accidentally joining a cluster, without being configured appropriately.

If you prefer using ElasticSearch inside a docker, see
[ElasticSearch inside a Docker](#elasticsearch-inside-a-docker).

### ElasticSearch configuration

It is **highly recommended** to avoid exposing this service to an untrusted zone.

If ElasticSearch and TheHive run on the same host (and not in a docker), edit `/etc/elasticsearch/elasticsearch.yml` and
set `network.host` parameter with `127.0.0.1`.
TheHive use dynamic scripts to make partial updates. Hence, they must be activated using `script.inline: on`.

The cluster name must also be set ("hive" for example).

Threadpool queue size must be set with a high value (100000). The default size will get the queue easily overloaded.

Edit `/etc/elasticsearch/elasticsearch.yml` and add the following lines:

```
network.host: 127.0.0.1
script.inline: on
cluster.name: hive
thread_pool.index.queue_size: 100000
thread_pool.search.queue_size: 100000
thread_pool.bulk.queue_size: 100000
```

### Start the Service
Now that ElasticSearch is configured, start it as a service and check whether it's running:
```
sudo systemctl enable elasticsearch.service
sudo systemctl start elasticsearch.service
sudo systemctl status elasticsearch.service
```

The status should be `active (running)`. If it's not running, you can check for the reason in the logs:
```
sudo journalctl -u elasticsearch.service
```

Note that by default, the database is stored in `/var/lib/elasticsearch` and the logs in `/var/log/elasticsearch`

## ElasticSearch inside a Docker

You can also start ElasticSearch inside a docker. Use the following command and do not forget to specify the absolute
path for persistent data on your host :

```
docker run \
  --name elasticsearch \
  --hostname elasticsearch \
  --rm \
  --publish 127.0.0.1:9200:9200 \
	--publish 127.0.0.1:9300:9300 \
  --volume ***DATA_DIR***:/usr/share/elasticsearch/data \
	-e "http.host=0.0.0.0" \
	-e "transport.host=0.0.0.0" \
	-e "xpack.security.enabled=false" \
	-e "cluster.name=hive" \
  -e "script.inline=true" \
  -e "thread_pool.index.queue_size=100000" \
  -e "thread_pool.search.queue_size=100000" \
  -e "thread_pool.bulk.queue_size=100000" \
	docker.elastic.co/elasticsearch/elasticsearch:5.5.2
```
