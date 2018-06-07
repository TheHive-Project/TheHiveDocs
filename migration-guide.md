# Migration guide


## From 3.0.x to 3.0.4

TheHive 3.0.4 (Cerana 0.4) comes with new MISP settings to filter events that will be imported as alerts. Please refer to [MISP event filters](admin/configuration.md#73-event-filters) configuration section.
The maximum number of custom fields and metrics in a case is 50 by default. If you try to put more, ElasticSearch will raise an error. You can now increase the limit by adding in your application.conf:
```
index {
  settings {
    # Maximum number of nested fields
    mapping.nested_fields.limit = 100
  }
}
```
The data schema has been changed in Cerana to support some dashboard features. At the first connection, TheHive will ask you to migrate the data. A new index, called `the_hive_13` by default, will be created then.  See
[Updating](admin/updating.md).

## From 2.13.x to 3.0.0

The schema of data has been changed in Cerana to integrate dashboard. At the first request, TheHive will ask you to migrate the data. A new index, called `the_hive_12` by default, will be created then.  See
[Updating](admin/updating.md).

## From 2.13.0 or 2.13.1 to 2.13.2

At the first connection to TheHive 2.13.2, a migration of the database will be
asked. This will create a new ElasticSearch index (`the_hive_11` by default). See
[Updating](admin/updating.md).

## From 2.12.x to 2.13.x

### Configuration updates

`play.crypto.secret` is deprecated, use `play.http.secret.key` instead.

`auth.type` is deprecated, use `auth.provider` instead.

**Basic authentication is disabled by default. We strongly recommand to update the clients that rely on the API to interact with TheHive to use the new API key authentication method**. This feature has been added in this release. If you need to enable
basic authentication, use `auth.method.basic=true` in `application.conf`

Note that the [TheHive4Py 1.3.0](https://github.com/TheHive-Project/TheHive4py) Python library also adds
API key authentication support.

### Alert role
A new role "alert" has been added. Only users with this role can create an
alert. If you have tool that uses TheHive API to create alerts, you must give
the ability to do it in user administration.

### ElasticSearch

TheHive 2.13 uses ElasticSearch 5.x. Our tests have been done on ElasticSearch
5.5. So we recommend to use this specific version, even if TheHive should work
perfectly with ElasticSearch 5.6 that doesn't introduce breaking changes.

#### Data structure migration
Before upgrading ElasticSearch, [backup all your indices](admin/backup-restore.md).
Then remove all indices except the last index of TheHive (most probably
the_hive_10). You can list all indices with the following command:

`curl http://127.0.0.1:9200/_cat/indices`

ElasticSearch has changed the structure of its data directory (please refer to
[Path to data on disk](https://www.elastic.co/guide/en/elasticsearch/reference/current/_path_to_data_on_disk.html)).
The node name in the path where data are stored (DATA_DIR) must be removed.
Stop ElasticSearch and execute the following lines to change the directory
structure:
```
echo -n 'Enter the path of ElasticSearch data: '
read DATA_DIR
echo -n 'Enter the name of your cluster [hive]: '
read CLUSTER_NAME

mv ${DATA_DIR}/${CLUSTER_NAME:=hive}/* ${DATA_DIR}
rmdir ${DATA_DIR}/${CLUSTER_NAME}
```

#### System requirements
ElasticSearch 5.x requires at least 262144 memory map areas (vm.max_map_count).
Run sysctl -w vm.max_map_count=262144. To make this setting persistent after a
server restart, add `vm.max_map_count = 262144` in `/etc/sysctl.conf` (or to
`/etc/sysctl.d/80-elasticsearch.conf`)

#### Configuration
The configuration of ElasticSearch should contain the following settings:
```
http.host: 127.0.0.1
transport.host: 127.0.0.1
cluster.name: hive
script.inline: true
thread_pool.index.queue_size: 100000
thread_pool.search.queue_size: 100000
thread_pool.bulk.queue_size: 100000
```
Adapt `http.host` and `transport.host` to your environment.

#### Docker
The default [ElasticSearch image](https://store.docker.com/images/elasticsearch) has
been deprecated. It is recommended to use the
[docker image from Elastic.co](docker.elastic.co/elasticsearch/elasticsearch).

The new image doesn't use the same user ID so you need to change the owner of the data
files. You can simply run `chown -R 1000.1000 $DATA_DIR` (DATA_DIR is the folder
which contains ElasticSearch data).

Then you can use the following script:
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

**Note**: TheHive doesn't support X-Pack. **Don't enable it**.

#### Warnings You Can Safely Ignore with ES 5.5
ElasticSearch 5.5 will output the following warnings:
 - `unexpected docvalues type NONE for field '_parent' (expected one of [SORTED, SORTED_SET]). Re-index with correct docvalues type.`
 You can safely ignore this message. For more information see issues [#25849](https://github.com/elastic/elasticsearch/issues/25849)
 and [#26341](https://github.com/elastic/elasticsearch/issues/26341)
 - `License [will expire] on [***]. If you have a new license, please update it.`
 Ignore this warning as TheHive doesn't use Elasticsearch's commercial features.

**Note**: ElasticSearch 5.6 fixes those warnings.

## From 2.11.x to 2.12.x

### Database migration

At the first connection to TheHive 2.12, a migration of the database will be
asked. This will create a new ElasticSearch index (the_hive_10). See
[Updating](admin/updating.md).

## From 2.10.x to 2.11.x

### Database migration

At the first connection to TheHive 2.11, a migration of the database will be
asked. This will create a new ElastciSearch index (the_hive_9). See
[Updating](admin/updating.md).

### MISP to alert

MISP synchronization is now done using alerting framework. MISP events are seen
like other alert. You can use
[TheHive4py](https://github.com/TheHive-Project/TheHive4py) to create your own alert.

### Configuration changes

#### MISP certificate authority deprecated

Specifying certificate authority in MISP configuration using "cert" key is now
deprecated. You must replace it by
- before:
```
misp {
  [...]
  cert = "/path/to/truststore.jks"
}
```
- after:
```
misp {
  [...]
  ws.ssl.trustManager.stores = [
    {
      type: "JKS"
      path: "/path/to/truststore.jks"
    }
  ]
}
```

`ws` key can be placed in MISP server section or in global MISP section. In the
latter, ws configuration will be applied
on all MISP instances.

#### Cortex and MISP HTTP client options

HTTP client used by Cortex and MISP is more configurable. Proxy can be
configured, with or without authentication. Refer to
[configuration](admin/configuration.md#8-http-client-configuration) for all
possible options.

### Packages

#### New RPM and DEB packages

RPM and DEB packages are now available. This makes the installation easier than using a
binary package (ZIP). See the [Installation Guide](installation/install-guide.md) for reference.

#### Docker

All-in-One docker (containing TheHive and Cortex) is not provided any longer.
New TheHive docker image doesn't contain ElasticSearch. We recommend to use
docker-compose to link TheHive, ElasticSearch and Cortex dockers. For more
information, see the [Installation Guide](installation/install-guide.md) for reference.

TheHive configuration is located in `/etc/thehive/application.conf` for all
packages. If you use docker package you must update its location (previously was
`/opt/docker/conf/application.conf`).
