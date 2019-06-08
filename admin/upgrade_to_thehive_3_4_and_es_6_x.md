This document is related to upgrading TheHive and Elasticsearch on **Ubuntu 16.04**.

### Upgrade TheHive to version 3.4

#### Perform a backup of data

```bash
curl -XPUT 'http://localhost:9200/_snapshot/the_hive_backup' -d '{
    "type": "fs",
    "settings": {
        "location": "/absolute/path/to/backup/directory",
        "compress": true
    }
}'
```

For example: 

```bash
curl -XPUT 'http://localhost:9200/_snapshot/the_hive_backup' -d '{
    "type": "fs",
    "settings": {
        "location": "/opt/backup",
        "compress": true
    }
}'
```

Next:

```bash
curl -XPUT 'http://localhost:9200/_snapshot/the_hive_backup/snapshot_1?wait_for_completion=true&pretty' -d '{
  "indices": "<INDEX>"
}'
```

For example:

```bash
curl -XPUT 'http://localhost:9200/_snapshot/the_hive_backup/the_hive_152019060701_1?wait_for_completion=true&pretty' -d '{
  "indices": "the_hive_15"
}'
```

Output example:

```json
{
  "snapshot" : {
    "snapshot" : "the_hive_152019060701_1",
    "uuid" : "ZKhBL2BHTAS2g71Xby2OgQ",
    "version_id" : 5061699,
    "version" : "5.6.16",
    "indices" : [
      "the_hive_15"
    ],
    "state" : "SUCCESS",
    "start_time" : "2019-06-07T13:07:38.844Z",
    "start_time_in_millis" : 1559912858844,
    "end_time" : "2019-06-07T13:07:40.640Z",
    "end_time_in_millis" : 1559912860640,
    "duration_in_millis" : 1796,
    "failures" : [ ],
    "shards" : {
      "total" : 5,
      "failed" : 0,
      "successful" : 5
    }
  }
}
```



You can find more information about backup and restore in the [dedicated documentation](https://github.com/TheHive-Project/TheHiveDocs/blob/master/admin/backup-restore.md). 

#### Stop TheHive service

```bash
service thehive stop
```

#### Update TheHive configuration

Current `/etc/thehive/application.conf`

```
# Elasticsearch
search {
  ## Basic configuration
  # Index name.
  index = the_hive
  # ElasticSearch cluster name.
  cluster = hive
  # ElasticSearch instance address.
  #host = ["127.0.0.1:9300"]
[..]
}
```

New /etc/thehive/application.conf :

```
 Elasticsearch
search {
  ## Basic configuration
  # Index name.
  index = the_hive
  # ElasticSearch instance address.
  uri = "http://127.0.0.1:9200"
  []
}

cluster {
  name = hive
}
```

#### Upgrade TheHive

```bash
apt upgrade thehive
```

#### Restart TheHive service

Ensure everything is working.

### Upgrade Elasticsearch from version 5.x to 6.x

This is greatly inspired by the official documentation : https://www.elastic.co/guide/en/elasticsearch/reference/6.0/rolling-upgrades.html with additional info we had to set up to make everything work.

Upgrading from earlier 5.x versions requires a [full cluster restart](https://www.elastic.co/guide/en/elasticsearch/reference/6.0/restart-upgrade.html). 

#### Disable shard allocation

```bash
curl -X PUT "localhost:9200/_cluster/settings" -H 'Content-Type: application/json' -d'
{
  "persistent": {
    "cluster.routing.allocation.enable": "none"
  }
}
'
```

Output:

```
{"acknowledged":true,"persistent":{"cluster":{"routing":{"allocation":{"enable":"none"}}}},"transient":{}}
```



```bash
curl -X POST "localhost:9200/_flush/synced"
```

Output :

```
{"_shards":{"total":60,"successful":30,"failed":0},"cortex_4":{"total":10,"successful":5,"failed":0},"cortex_2":{"total":10,"successful":5,"failed":0},"cortex_3":{"total":10,"successful":5,"failed":0},"the_hive_13":{"total":10,"successful":5,"failed":0},"the_hive_15":{"total":10,"successful":5,"failed":0},"the_hive_14":{"total":10,"successful":5,"failed":0}}
```

#### shut down a single node

```bash
sudo -i service elasticsearch stop
```

#### Upgrade the node you shut down

```bash
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
sudo apt-get install apt-transport-https
echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-6.x.list
sudo apt-get update && sudo apt-get install elasticsearch
```

#### Upgrade plugins 

```bash
/usr/share/elasticsearch/bin/elasticsearch-plugin list
## for all plugin:
/usr/share/elasticsearch/bin/elasticsearch-plugin install $plugin
```

#### Update Elasticsearch configuration

Add `path.logs` and `path.data` in `/etc/elasticsearch/elasticsearch.yml:

```yaml
http.host: 127.0.0.1
transport.host: 127.0.0.1
cluster.name: hive
thread_pool.index.queue_size: 100000
thread_pool.search.queue_size: 100000
thread_pool.bulk.queue_size: 100000
path.repo: ["/opt/backup"]
path.logs: "/var/log/elasticsearch"
path.data: "/var/lib/elasticsearch"
```

Set `$JAVA_HOME` in `/etc/default/elasticsearch` for example:

```
[..]
JAVA_HOME=/usr/lib/jvm/java-8-oracle/
[..]
```

On Ubuntu 16.04 we had to set read persmissions manually to this file: 

```bash
chmod o+r /etc/default/elasticsearch
```

#### Restart the node

```bash
sudo update-rc.d elasticsearch defaults 95 10
sudo -i service elasticsearch start

```

#### Check that elasticsearch is running 

```bash
curl -X GET "localhost:9200/"
curl -X GET "localhost:9200/_cat/nodes"
```

#### Reenable shard allocation

Once the node has joined the cluster:

```bash
curl -X PUT "localhost:9200/_cluster/settings" -H 'Content-Type: application/json' -d'
{
  "persistent": {
    "cluster.routing.allocation.enable": null
  }
}
'
```

Output:

```
{"acknowledged":true,"persistent":{},"transient":{}}
```



#### Wait for the node to recover

Before upgrading the next node, wait for the cluster to finish shard allocation. You can check progress by submitting a [`_cat/health`](https://www.elastic.co/guide/en/elasticsearch/reference/6.0/cat-health.html) request:

```bash
curl -X GET "localhost:9200/_cat/health?v"
```

### Resources

- https://www.elastic.co/guide/en/elasticsearch/reference/6.0/rolling-upgrades.html
- https://www.elastic.co/guide/en/elasticsearch/reference/6.0/restart-upgrade.html
- https://www.elastic.co/guide/en/elasticsearch/reference/6.0/deb.html