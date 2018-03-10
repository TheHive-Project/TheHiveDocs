# Backup and restore data
All persistent data is stored in an Elasticsearch database. The backup and restore procedures are the ones that are
detailed in
[Elasticsearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-snapshots.html).

_Note_: you may have to adapt your indices in the examples below. To find the right index, use the following command :

```
curl 'localhost:9200/_cat/indices?v'
```

You can also refer to the [schema version](schema_version.md) page.

To save all your data you only need to backup the last indice. For example, if the previous command gives you the following results, all your data belongs to **the_hive_12**.

```
health status index                         uuid                   pri rep docs.count docs.deleted store.size pri.store.size
yellow open   the_hive_11                   HVVYDC68SrGAfSbcjVPZWg   5   1      43018           17     24.9mb         24.9mb
yellow open   the_hive_12                   Cq4Gc4qkRPaTCqrorFgDRw   5   1      43226            0     25.3mb         25.3mb
```


**In the rest of this document, ensure to change <INDEX> to your own last index in order to backup or restore all your data.**


## 1. Create a backup repository

First you must define a location in local filesystem (where Elasticsearch instance runs) where the backup will be written. This repository must be declared in the Elasticsearch configuration. Edit _elasticsearch.yml_ file by adding:

```
path.repo: ["/absolute/path/to/backup/directory"]
```

Then, restart the Elasticsearch service.


_Note_: Be careful if you run Elasticsearch in Docker, the directory must be mapped in host filesystem using `--volume`
parameter (cf. [Docker documentation](https://docs.docker.com/engine/tutorials/dockervolumes/)).


## 2. Register a snapshot repository

Create an Elasticsearch snapshot point named *the_hive_backup* with the following command (set the same path in the location setting as the one set in the configuration file):

```
$ curl -XPUT 'http://localhost:9200/_snapshot/the_hive_backup' -d '{
    "type": "fs",
    "settings": {
        "location": "/absolute/path/to/backup/directory",
        "compress": true
    }
}'
```

The result of the command should look like this :

```
{"acknowledged":true}
```

Since, everything is fine to backup and restore data.


## 3. Backup your data

Create a backup named *snapshot_1* of all your data by executing the following command :

```
$ curl -XPUT 'http://localhost:9200/_snapshot/the_hive_backup/snapshot_1?wait_for_completion=true&pretty' -d '{
  "indices": "<INDEX>"
}'
```
This command terminates only when the backup is complete and the result of the command should look like this:

```
{
  "snapshots": [{
    "snapshot": "snapshot_1",
    "uuid": "ZQ3kv5-FQoeN3NFIhfKgMg",
    "version_id": 5060099,
    "version": "5.6.0",
    "indices": ["the_hive_12"],
    "state": "SUCCESS",
    "start_time": "2018-01-29T14:41:51.580Z",
    "start_time_in_millis": 1517236911580,
    "end_time": "2018-01-29T14:42:05.216Z",
    "end_time_in_millis": 1517236925216,
    "duration_in_millis": 13636,
    "failures": [],
    "shards": {
      "total": 41,
      "failed": 0,
      "successful": 41
    }
  }]
}
```


_Note_:
You can backup the last index of TheHive (you can list indices in your Elasticsearch cluster with
`curl -s http://localhost:9200/_cat/indices | cut -d ' '  -f3` ) or all indices with `_all` value.


## 4. Restore data

Restore will do the reverse actions : it reads the backup in your snapshot directory and loads indices into the Elasticsearch
cluster. This operation is done with the following command :
```
$ curl -XPOST 'http://localhost:9200/_snapshot/the_hive_backup/snapshot_1/_restore' -d '
{
  "indices": "<INDEX>"
}'
```

The result of the command should look like this :

```
{"accepted":true}
```

_Note_: be sure to restore data from the same version of Elasticsearch.


## 5. Moving data from one server to another

If you want to move your data from one server from another:
- Create your backup on the origin server (steps [1](1__create_a_backup_repository), [2](2__register_a_snapshot_repository), [3](3__backup_your_data))
- copy your backup directory from the origin server to the destination server
- On the destination server :
    - Register your backup repository in the Elasticsearch configuration (step [1](1__create_a_backup_repository))
    - Register your snapshot repository with the same snapshot name (step [2](2__register_a_snapshot_repository))
    - Restore your data (step [4](4__restore_data))
