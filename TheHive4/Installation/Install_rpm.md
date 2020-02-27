# Installation Guide on RedHat-like OS

This page is a step by step installation and configuration guide to get an TheHive 4 instance up and running on systems using DEB packages repositories.

## Java Virtual Machine


```bash
yum install -y java-1.8.0-openjdk-headless.x86_64
echo JAVA_HOME="/usr/lib/jvm/jre-1.8.0" >> /etc/environment
export JAVA_HOME="/usr/lib/jvm/jre-1.8.0"
```


## Cassandra database

Apache Cassandra is a scalable and high available database. TheHive supports version  **3.11.x** of Cassandra.

### Install from repository

- Add the Apache repository of Cassandra to `/etc/yum.repos.d/cassandra.repo`

```bash
[cassandra]
name=Apache Cassandra
baseurl=https://downloads.apache.org/cassandra/redhat/311x/
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://downloads.apache.org/cassandra/KEYS
```

- Install the package

```bash
yum install -y cassandra
```

By default, data is stored in `/var/lib/cassandra`.

### Configuration

Start by changing the `cluster_name` with `thp`. Run the command `sqlsh`: 

```bash
UPDATE system.local SET cluster_name = 'thp' where key='local';
```

Then run: 

```
nodetool flush
```

Configure Cassandra by editing `/etc/cassandra/conf/cassandra.yaml` file. 


```yml
# content from /etc/cassandra/conf/cassandra.yaml

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



Run the service and ensure it restart after a reboot:

```bash
systemctl daemon-reload
service cassandra start
chkconfig cassandra on
```

By default Cassandra listens on `7000/tcp` (inter-node), `9042/tcp` (client).

---

⚠️ **Note**

Cassandra service does not start well with the new systemd version. There is an existing issue and a fix on Apache website: https://issues.apache.org/jira/browse/CASSANDRA-15273 

---

#### Additional configuration

For additional configuration options, refer to:

- [Cassandra documentation page](https://cassandra.apache.org/doc/latest/getting_started/configuring.html)
- [Datastax documentation page](https://docs.datastax.com/en/ddac/doc/datastax_enterprise/config/configTOC.html)


#### Security

To add security measures in Cassandra , refer the the [related administration guide](../Administration/Cassandra_security.md).

#### Add nodes

To add Cassandra nodes, refer the the [related administration guide](../Administration/Clustering.md).

## Choose and install attachment storage

Files uploaded in TheHive (in *task logs* or in *observables*) can be stores in localsystem, in a Hadoop filesystem (recommended) or in the graph database. 

For standalone production and test servers , we recommends using local filesystem. If you think about building a cluster with TheHive, use Hadoop filesystem.

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
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
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

- The configuration described there is for a single node server. This node is the master node, namenode and datanode (refer to [Hadoop documentation](https://hadoop.apache.org/docs/current/) for more information). After validating this node is running successfully, refer to the [related administration guide](../Administration/Clustering.md) to add nodes;
- Ensure you **update** the port value to something different than `9000` as it is already reserved for TheHive application service;


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

Create the `/etc/systemd/system/hadoop.service` file with the following content: 

```
[Unit]
Description=Hadoop
Documentation=https://hadoop.apache.org/docs/current/index.html
Wants=network-online.target
After=network-online.target

[Service]
WorkingDirectory=/opt/hadoop
Type=forking

User=hadoop
Group=hadoop
Environment=JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
Environment=HADOOP_HOME=/opt/hadoop
Environment=YARN_HOME=/opt/hadoop
Environment=HADOOP_COMMON_HOME=/opt/hadoop
Environment=HADOOP_HDFS_HOME=/opt/hadoop
Environment=HADOOP_MAPRED_HOME=/opt/hadoop
Restart=on-failure

TimeoutStartSec=2min


ExecStart=/opt/hadoop/sbin/start-all.sh
ExecStop=/opt/hadoop/sbin/stop-all.sh

StandardOutput=null
StandardError=null

# Specifies the maximum file descriptor number that can be opened by this process
LimitNOFILE=65536

# Disable timeout logic and wait until process is stopped
TimeoutStopSec=0

# SIGTERM signal is used to stop the Java process
KillSignal=SIGTERM

# Java process is never killed
SendSIGKILL=no

[Install]
WantedBy=multi-user.target
```



#### Start the service 

```bash
service hadoop start
```


You can check cluster status in [http://thehive1:9870](http://thehive1:9870/)

#### Add nodes

To add Hadoop nodes, refer the the [related administration guide](../Administration/Clustering.md).


## TheHive

This part contains instructions to install TheHive and then configure it.

---

⚠️ **Note**

TheHive4 can't be installed on the same OS than older versions.

---


### Installation

RPM packages are published on a our RPM repository. All packages are signed using our GPG key [562CBC1C](https://raw.githubusercontent.com/TheHive-Project/TheHive/master/PGP-PUBLIC-KEY). Its fingerprint is:

`0CD5 AC59 DE5C 5A8E 0EE1  3849 3D99 BB18 562C BC1C`

Run the following command to import the GPG key :

```bash
sudo rpm --import https://raw.githubusercontent.com/TheHive-Project/TheHive/master/PGP-PUBLIC-KEY
```

And setup your system to connect the RPM repository. Create and edit the file `/etc/yum.repo.d/thehive-project.repo`: 

```bash
[thehive-project]
enabled=1
priority=1
name=TheHive-Project RPM repository
baseurl=http://rpm.thehive-project.org/beta/noarch
gpgcheck=1
```

Then you will able to install the package using `yum`:
```bash
yum install thehive4
```

### Configuration

#### Minimal required configuration

The only required parameter in order to start TheHive is the key of the server (`play.http.secret.key`). This key is used to authenticate cookies that contain data. If TheHive runs in cluster mode, all instances must share the same key.

Setup a secret key in the `/etc/thehive/conf/application.conf` file:

```
play.http.secret.key:<SECRET_KEY>
```

This secret key is a random string, you can generate one with the following command:

```bash
cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1
```

#### Database

To use Cassandra database, TheHive configuration file (`/etc/thehive/conf/application.conf`) has to be edited and updated with following lines:

```yaml
db {
  provider: janusgraph
  janusgraph {
    storage {
      backend: cql
      hostname: [
        "127.0.0.1"
      ] # seed node ip addresses

      #username: "<cassandra_username>"       # login to connect to database (if configured in Cassandra)
      #password: "<cassandra_passowrd"

      cql {
        cluster-name: thp       # cluster name
        keyspace: thehive           # name of the keyspace
        local-datacenter: datacenter1   # name of the datacenter where TheHive runs (relevant only on multi datacenter setup)
        # replication-factor: 2 # number of replica
        read-consistency-level: ONE
        write-consistency-level: ONE
      }
    }
  }
}
```

#### Local filesystem

If you chose [Option 1: Local filesystem](#option:1_local_filesystem) to store files:

- Update permission of the folder

```bash
chown -R thehive:thehive /opt/thp_data/files/thehive
```

- add following lines to TheHive configuration file (`/etc/thehive/conf/application.conf`)

```yml
storage {
  provider = localfs
  localfs.directory = /opt/files/thehive
}
```

#### Hadoop

If you chose [Option 2: Hadoop](#option:2_hadoop) to store files in a distrubuted filesystem, add following lines to TheHive configuration file (`/etc/thehive/conf/application.conf`)

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

Save configuration file and run the service:

```
service thehive start
```

## Advanced configuration

For additional configuration options, please refer to the [Administration Guide](/admin/admin-guide.md).

