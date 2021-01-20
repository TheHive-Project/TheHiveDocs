# Migration from Elasticsearch 6.8.2 to ES 7.x

---
⚠️ IMPORTANT NOTE

- This migration process is intended for single node of Elasticsearch database
- The current version of this document is provided for testing purpose **ONLY!**  
- This guide has been written and tested to migrate data from ES 6.8.2 to ES 7.8.1, and TheHive 3.4.2 to TheHive 3.5.0-RC1 **only!**
- This guide starts with Elasticsearch version 6.8.2  up and running, indexes and data. To test this guide, we recommend using a backup of you production server. (see [Backup and Restore page](./backup-restore.md) for more information)
- This guide is illustrated with TheHive index. The process is identical for Cortex, you just have to adjust index names.
---

## Prerequisite

The software `jq` is required to manipulate JSON and create new indexes. More information at [https://stedolan.github.io/jq/](). 

## Identify if your index should be reindexed

You can easily identify if indexes should be reindexed or not. On the index named `the_hive_15` run the following command: 

```
curl -s http://127.0.0.1:9200/the_hive_15?human | jq '.the_hive_15.settings.index.version.created'
```

if the output is similar to `"5xxxxxx"`  then reindexing is required, you should follow this guide. 

If it is   `"6xxxxxx"` then the index can be read by Elasticsearch 7.8.x. Upgrade Elasticsearch, and TheHive-3.5.0.

## Migration guide

### Current status

Current context is: 
- Elasticsearch 6.8.2
- TheHive 3.4.2

All up and running. 

Start by identifying indices on you Elasticsearch instance.

```
curl  http://localhost:9200/_cat/indices\?v
```

The output should look like this: 

```
health status index           uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   the_hive_15     Oap-I61ySgyv6EAI1ZUTFQ   5   0      30977           36     33.2mb 
```


The index name is `the_hive_15`. Record this somewhere.

### Stop services

Before starting updating the database, lets stop applications:

```
sudo service thehive stop 
```

### Create a new index


The First operation lies in creating a new index named `new_the_hive_15` with settings from current index `the_hive_15` (ensure to keep index version, needed for future upgrade).

```bash
curl -XPUT 'http://localhost:9200/new_the_hive_15' \
  -H 'Content-Type: application/json' \
  -d "$(curl http://localhost:9200/the_hive_15 |\
   jq '.the_hive_15 |
   del(.settings.index.provided_name,
    .settings.index.creation_date,
    .settings.index.uuid,
    .settings.index.version,
    .settings.index.mapping.single_type,
    .mappings.doc._all)'
    )"
```


Check the new index is well created: 

```
curl -XGET http://localhost:9200/_cat/indices\?v
```

The output should look like this: 

```
health status index           uuid                   pri rep docs.count docs.deleted store.size pri.store.size
yellow open   new_the_hive_15 A2KLoZPpSXygutlfy_RNCQ   5   1          0            0      1.1kb          1.1kb
green  open   the_hive_15     Oap-I61ySgyv6EAI1ZUTFQ   5   0      30977           36     33.2mb         33.2mb
```

### Proceed to Reindex 

Next operation lies in running the reindex command in the newly created index:

```bash
curl -XPOST -H 'Content-Type: application/json' http://localhost:9200/_reindex -d '{
  "conflicts": "proceed",
  "source": {
    "index": "the_hive_15"
  },
  "dest": {
    "index": "new_the_hive_15"
  }
}'
```

After a moment, you should get a similar output:  

```json
{
    "took": 5119,
    "timed_out": false,
    "total": 5889,
    "updated": 0,
    "created": 5889,
    "deleted": 0,
    "batches": 6,
    "version_conflicts": 0,
    "noops": 0,
    "retries": {
        "bulk": 0,
        "search": 0
    },
    "throttled_millis": 0,
    "requests_per_second": -1.0,
    "throttled_until_millis": 0,
    "failures": []
}
```

### Ensure new index has been created

Run the following command, and ensure the new index is like the current one (size can vary):

```
curl -XGET http://localhost:9200/_cat/indices\?v
```

The output should look like this: 

```
health status index           uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   new_the_hive_15 GV-3Y8QjTjWw0F-p2sjW6Q   5   0      30977            0       26mb           26mb
green  open   the_hive_15     Oap-I61ySgyv6EAI1ZUTFQ   5   0      30977           36     33.2mb         33.2mb
```

### Delete old indices

This is the thrilling part. 
Now the new index `new_the_hive_15` is created and similar the_hive_15,  older indexes **should be completely deleted** from the database. To delete index named `the_hive_15`, run the following command:  

```bash
curl -XDELETE http://localhost:9200/the_hive_15
```

Run the same command for older indexes if exist (the_hive_14, the_hive_13....). Elasticsearch 7.x cannot run with index created with Elasticsearch 5.x.

### Create an alias 

Before stopping Elasticsearch service, let’s create an alias to keep index names in the future.  

```bash
curl -XPOST -H 'Content-Type: application/json'  'http://localhost:9200/_aliases' -d '{
    "actions": [
        {
            "add": {
                "index": "new_the_hive_15",
                "alias": "the_hive_15"
            }
        }
    ]
}'
```


Doing so will allow TheHive 3.5.0 to find the index without updating the configuration file. 

Check the alias has been well created by running the following command

```bash
curl -XGET http://localhost:9200/_alias?pretty
```

The output should look like:

```json
{
  "new_the_hive_15" : {
    "aliases" : {
      "the_hive_15" : { }
    }
  }
}
```


## Stop Elasticsearch version 6.8.2

```bash
sudo service elasticsearch stop 
```


## Update Elasticsearch 

Update the configuration of Elastisearch. Configuration file should look like this:

```
[..]
http.host: 127.0.0.1
discovery.type: single-node
cluster.name: hive
script.allowed_types: inline
thread_pool.search.queue_size: 100000
thread_pool.write.queue_size: 10000    
```

Now, upgrade Elasticsearch to version 7.x following the documentation for your Operating System, and ensure the service start successfully.

## Install or update to TheHive 3.5.0

### DEB package

If using Debian based Linux operating system, configure it to follow our beta repository:

```bash
curl https://raw.githubusercontent.com/TheHive-Project/TheHive/master/PGP-PUBLIC-KEY | sudo apt-key add -
echo 'deb https://deb.thehive-project.org release main' | sudo tee -a /etc/apt/sources.list.d/thehive-project.list
sudo apt-get update
```
Then install it by running:

```bash
sudo apt install thehive
```

or

```bash
sudo apt install thehive=3.5.0-1
```

### RPM

Setup your system to connect the RPM repository. Create and edit the file  `/etc/yum.repos.d/thehive-project.repo` :

```
[thehive-project]
enabled=1
priority=1
name=TheHive-Project RPM repository
baseurl=http://rpm.thehive-project.org/release/noarch
gpgcheck=1
```

Then install it by running:

```bash
sudo yum install thehive
```

or 

```bash
sudo yum install thehive-3.5.0-1
```

### Install binaries

```bash
cd /opt
wget https://download.thehive-project.org/thehive-3.5.0-1.zip
unzip thehive-3.5.0-1.zip
ln -s thehive-3.5.0-1 thehive
```

### Docker images

Docker images are also provided on Dockerhub. 

```bash
docker pull thehiveproject/thehive:3.5.0-1
```

### Update Database

Connect to TheHive, the maintenance page should ask to update. 

![](/images/thehive-first-access_screenshot.png)

Once updated, ensure a new index named `the_hive_16` has been created.


```bash
curl -XGET http://localhost:9200/_cat/indices\?v
```

The output should look like this: 

```
health status index           uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   new_the_hive_15 GV-3Y8QjTjWw0F-p2sjW6Q   5   0      30977            0       26mb           26mb
yellow open   the_hive_16     Nz0vCKqhRK2xkx1t_WF-0g   5   1      30977            0     26.1mb         26.1mb
```

