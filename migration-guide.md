# Migration guide


## From 3.4.x to 3.5.0

Taking into account the EoL of version 6.x. of Elasticsearch, TheHive 3.5.0 is the first version to support Elasticsearch 7.x. This version introduce breaking changes.  This time,  we had no choice, we were not able to make TheHive support smoothly the ES upgrade. 

TheHive 3.5.0 supports Elasticsearch 7.x **ONLY**.

This first steps before starting the upgrade process are: 

- Identify the version of Elasticsearch which created your index
- Stop TheHive service
- Stop Elasticsearch service

### How to identify the version of Elasticsearch which created your database index ?

---

The software `jq` is required to manipulate JSON and create new indexes. More information at [https://stedolan.github.io/jq/](). 

---

Run the following command : 

```bash
curl -s http://127.0.0.1:9200/the_hive_15?human | jq '.the_hive_15.settings.index.version.created_string'
```

- if the output is similar to `"5.x"`  then your database index has been created with Elasticsearch 5.x  reindexing is required, you should follow [a dedicated process to upgrade](admin/upgrade_to_thehive_3_5_and_es_7_x.md). 
- If it is   `"6.x"` then your database has been created with Elasticsearch 6.

### Your database was created with Elasticsearch 5.x or earlier

This is where things might be complicated. This upgrade progress  requires handling the database index by updating parameters, and reindex before updating Elasticsearch, and updating TheHive.

Read carefully [the dedicated documentation](admin/upgrade_to_thehive_3_5_and_es_7_x.md). It should help you run this specific actions on your Elasticsearch database, and also install or update application whether you are using DEB, RPM or binary packages, and even docker images.

### Your database was created with Elasticsearch 6.x

If you started using TheHive with Elasticsearch 6.x, then you just need to update the configuration of Elasticsearch to reflect this one: 

```
[..]
http.host: 127.0.0.1
discovery.type: single-node
cluster.name: hive
script.allowed_types: inline
thread_pool.search.queue_size: 100000
thread_pool.write.queue_size: 10000
```

Following parameters **are not accepted anymore* by Elasticsearch 7: 

- `thread_pool.index.queue_size`
- `thread_pool.bulk.queue_size` 

With TheHive service stopped, ensure the new version of Elasticsearch starts.

If everything is ok, then TheHive 3.5.0 can be installed. To run this operation successfully, you need to **update your repository configuration**  if you are using DEB and RPM packages, or specify the right version to install if using docker. Read carefully the [installation guide](installation/install-guide.md). 


## From 3.3.x to 3.4.0
Starting from version 3.4.0-RC1, TheHive supports Elasticsearch 6 and will continue to work with Elasticsearch 5.x.
                        
TheHive 3.4.0-RC1 and later versions communicate with Elasticsearch using its HTTP service (9200/tcp by default) instead of its legacy binary protocol (9300/tcp by default). If you have a firewall between TheHive and Elasticsearch, you probably need to update its rules to change to the new port number.
                        
The configuration file (`application.conf`) needs some modifications to reflect the protocol change:

- The setting `search.host` is replaced by `search.uri`
- The general format of the URI is: `http(s)://host:port,host:port(/prefix)?querystring`. Multiple `host:port` combinations can be specified, separated by commas. Options can be specified using a standard URI query string syntax, eg. `cluster.name=hive`.
- The `search.cluster`setting is no longer used.
- Authentication can be configured with the `search.user` and `search.password` settings.

When SSL/TLS is enabled, you can set a truststore and a keystore. The truststore contains the certificate authorities used to validate remote certificates. The keystore contains the certificate and the private key used to connect to the Elasticsearch cluster. The configuration is:
```hocon
search {
  keyStore {
	path: "/path/to/keystore/file"
	type: "JKS" # or PKCS12
	password: "secret.password.of.keystore"
  }
  trustStore {
	path: "/path/to/truststore/file"
	type: "JKS"
	password: "secret.password.of.truststore"
  }
}
```

The Elasticsearch client also accepts the following settings:
 - `circularRedirectsAllowed` (`true`/`false`)
 - `connectionRequestTimeout` (number of seconds)
 - `connectTimeout`
 - `contentCompressionEnabled.foreach(requestConfigBuilder.setContentCompressionEnabled)`
 - `search.cookieSpec` (??)
 - `expectContinueEnabled` (`true`/`false`)
 - `maxRedirects` (number)
 - `proxy` -- not yet supported
 - `proxyPreferredAuthSchemes` -- not yet supported
 - `redirectsEnabled` (`true`/`false`)
 - `relativeRedirectsAllowed` (`true`/`false`)
 - `socketTimeout` (number of seconds)
 - `targetPreferredAuthSchemes` (??) 

The configuration items `keepalive`, `pageSize`, `nbshards` and `nbreplicas` are still valid.

For practical details, you can have a look [here](admin/upgrade_to_thehive_3_4_and_es_6_x.md) for an example of migration of TheHive and Elasticsearch.

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
