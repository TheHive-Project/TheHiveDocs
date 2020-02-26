# Installation Guide

This page is a step by step installation and configuration guide to get an TheHive 4 instance up and running.

## Java Virtual Machine


```bash
apt-get install -y openjdk-11-jre-headless
echo JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64/jre" >> /etc/environment
export JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64/jre"
```


## Cassandra database

Apache Cassandra is a scalable and high available database. TheHive supports version of  **3.11.x** of Cassandra.

### Install from repository

- Reference Apache repository

```bash
curl https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -
echo "deb http://www.apache.org/dist/cassandra/debian 311x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
```

- Install the package

```bash
apt update
apt install cassandra
```

By default, data is stored in `/var/lib/cassandra`.

### Install from Apache TGZ archive

Download and untgz archive from http://cassandra.apache.org/download/ in the folder of your choice.

### Configuration

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

#### Add nodes

To add Cassandra nodes, refer the the [related administration guide](../Administration/Clustering.md).

## Choose and install attachment storage

Files uploaded in TheHive (in *task logs* or in *observables*) can be stores in localsystem, in a Hadoop filesystem (recommended) or in the graph database. The localsystem can't be used on a cluster setup and the latter is discouraged as it has performance issue on large file.

### Option 1: Local filesystem

**Note**: This option is perfect if you **do not** intend to build a cluster for your instance of TheHive 4. 

To store files on the local filesystem, start by choosing the dedicated folder:

```bash
mkdir -p /opt/thp_data/files/thehive
```

This path will be used in the configuration of TheHive. 

Later, after having installed TheHive, ensure the user `thehive` owns the path chosen for storing files:

``` 
chown -R thehive:thehive /opt/thp_data/files/thehive
```

### Option 2: Hadoop

If you choose Hadoop distributed filesystem, proceed to installation of the software before configuring it.

#### Installation 

- Download hadoop distribution from https://hadoop.apache.org/releases.html and uncompress.

```bash
cd /tmp
wget https://downloads.apache.org/hadoop/common/hadoop-3.1.3/hadoop-3.1.3.tar.gz
cd /opt
tar zxf /tmp/hadoop-3.1.3.tar.gz
ln -s hadoop-3.1.3 hadoop
```

- Create a user and update permissions

```bash
useradd hadoop
chown hadoop:root -R /opt/hadoop*
```

- Create a datastore and set permissions

```bash
mkdir /opt/thp_data/hdfs
chown hadoop:root -R /opt/thp_data/hdfs
```

- Create ssh keys for `hadoop` user: 

```bash
su - hadoop
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys
```

- Update `.bashrc`file for `hadoop user  in `/etc/environment`. Add following lines: 

```
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export HADOOP_HOME=/opt/hadoop
export PATH=$PATH:$HADOOP_HOME/bin
export PATH=$PATH:$HADOOP_HOME/sbin
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
```


**Note**: Apache has a well detailed [documentation](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html) for more advanced configuration with Hadoop. 


#### Configuration the Hadoop Master

Configuration files are located in `etc/hadoop` (`/opt/hadoop/etc/hadoop`). They must be identical in all nodes. 

**Notes**: 
- Ensure you **update** the port value to something different than `9000` as it is already reserved for TheHive application service;
- **Only if you are using a standalone server**, hostname or address can be limited to `localhost` or `127.0.0.1` for the value of `fs.defaultFS` property. Else use the hostname of your machine ; 


- Edit the file `core-site.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://thehive1:10000</value>
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

#### Format the volume and start services

- Format  the volume

```bash
su - hadoop
cd /opt/hadoop
bin/hdfs namenode -format
```

#### Run it as a service

---

XXX TO BE UPDATED OR DELETED XXX

- Start the namenode

```bash
su - hadoop
cd /opt/hadoop
sbin/start-dfs.sh
```

---


You can check cluster status in [http://thehive1:9870](http://thehive1:9870/)



#### Add nodes

To add Hadoop nodes, refer the the [related administration guide](../Administration/Clustering.md).


## TheHive

### Installation

Choose the way or package relevant package repository for your system and installation TheHive 4 by following [this documentation](Packages_and_binaries.md). 

### Configuration 

#### Database

To use Cassandra database, TheHive configuration file (`/etc/thehive/conf/application.conf`) has to be edited and configured:

```yaml
db {
  janusgraph {
    storage.backend: cql
    storage.hostname: ["127.0.0.1"]
    # storage.username = new_super_user
    # storage.password = some_secure_password
    cql.read-consistency-level: ONE
    cql.write-consistency-level: ONE
  }
}
```

#### Filesystem

- Local filesystem : add following lines to TheHive configuration file (`/etc/thehive/conf/application.conf`)

```yml
storage {
  provider = localfs
  localfs.directory = /opt/files/thehive
}
```

- Hadoop filesystem

```yaml
storage {
  provider: hdfs
  hdfs {
    root: "hdfs://thehive1:10000" # namenode server
    location: "/thehive"
    username: thehive
  }
}
```


### Run

```
service thehive start
```

Then proceed to [installation](Installation.md) of TheHive and [configure](Base_configuration.md) everything before starting.

