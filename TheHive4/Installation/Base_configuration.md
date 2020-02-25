This part describes how to configure TheHive to quickly get it up and running. This configuration is for one standalone server (not cluster), without connections to Cortex or MISP. For more advanced configuration, refer to [administration guides](../README.md#administration_guides).



## Cassandra

By default, data is stored in `/var/lib/cassandra`.  

### Cassandra configuration

Configure Cassandra by editing `conf/cassandra.yaml`, or `/etc/cassandra/cassandra.yaml` with package installation 

**Notes**: 
- if data is set in another folder than the default one, change `/var/lib/cassandra` with your folder for data in the following configuration;
- For production purpose, it is recommended that commitlogs and data be in separated physical disk. Other settings can be let as is.

```yml
cluster_name: 'thp'
listen_address: 'xx.xx.xx.xx' # address for nodes
rpc_address: 'xx.xx.xx.xx' # address for clients
seed_provider:
    - class_name: org.apache.cassandra.locator.SimpleSeedProvider
      parameters:
          # Ex: "<ip1>,<ip2>,<ip3>"
          - seeds: 'xx.xx.xx.xx' # self for the first node
data_file_directories:
  - '/var/lib/cassandra/data'
commitlog_directory: '/var/lib/cassandra/commitlog'
saved_caches_directory: '/var/lib/cassandra/saved_caches'
hints_directory: '/var/lib/cassandra/hints'
```

Then, delete default data and restart the service: 

```bash
cd /var lib
rm -rf cassandra && mkdir cassandra && chown -R cassandra:cassandra cassandra
service cassandra restart
```

By default Cassandra listen on `7000/tcp` (inter-node), `9042/tcp` (client).

## Configure file storage

### Use host filesystem

Ensure the user `thehive` owns the path chosen for storing files:

``` 
chown -R thehive:thehive /opt/thp_data/files/thehive
```



### Use distributed filesystem

#### Hadoop

Configuration files are located in `etc/hadoop` (`/opt/hadoop/etc/hadoop`). They must be identical in all nodes. 

- Edit the file `core-site.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://127.0.0.1:10000</value>
  </property>
  <property>
    <name>hadoop.tmp.dir</name>
    <value>/opt/thp_data/hdfs/temp</value>
  </property>
  <property>
    <name>dfs.client.block.write.replace-datanode-on-failure.best-effort</name>
    <value>true</value>
  </property>
</configuration>
```

- Edit the file `hdfs-site.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>2</value>
  </property>
  <property>
    <name>dfs.namenode.name.dir</name>
    <value>/opt/thp_data/hdfs/namenode/data</value>
  </property>
  <property>
    <name>dfs.datanode.name.dir</name>
    <value>/opt/thp_data/hdfs/datanode/data</value>
  </property>
  <property>
    <name>dfs.namenode.checkpoint.dir</name>
    <value>/opt/thp_data/hdfs/checkpoint</value>
  </property>
  <property>
    <name>dfs.namenode.http-address</name>
    <value>0.0.0.0:9870</value>
  </property>
  <!--
  <property>
    <name>dfs.client.block.write.replace-datanode-on-failure.best-effort</name>
    <value>true</value>
  </property>
-->
  <property>
    <name>dfs.client.block.write.replace-datanode-on-failure.policy</name>
    <value>NEVER</value>
  </property>
</configuration>
```

On the namenode, format the volume

```bash
cd /opt/hadoop
bin/hdfs --config /opt/hadoop/etc/hadoop namenode -format
```

Start the namenode

```bash
bin/hdfs --config /opt/hadoop/etc/hadoop namenode
```

Start the datanode on all nodes

```bash
bin/hdfs --config /opt/hadoop/etc/hadoop datanode
```

You can check cluster status in [http://namenode:9870](http://namenode:9870/)

## Configure TheHive and get it ready to start
