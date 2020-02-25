# Prepare your environment

For the purpose of the documentation


## Install Java JRE 8+


```bash
apt-get install -y openjdk-8-jre-headless
```

## Install Cassandra database

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


### Install from Apache TGZ archive

Download and untgz archive from http://cassandra.apache.org/download/ in the folder of your choice.

## Choose and install attachment storage

Files uploaded in TheHive (in *task logs* or in *observables*) can be stores in localsystem, in a Hadoop filesystem (recommended) or in the graph database. The localsystem can't be used on a cluster setup and the latter is discouraged as it has performance issue on large file.

### Local filesystem

If you choose to store files oon the local filesystem, start by choosing the dedicated folder:

```bash
mkdir -p /opt/thp_data/files/thehive
```

This path will be used in the configuration of TheHive. 

### Hadoop

If you choose Hadoop distributed filesystem, proceed to installation of the software before configuring it.

Download hadoop distribution from https://hadoop.apache.org/releases.html and uncompress.

```bash
cd /tmp
wget https://downloads.apache.org/hadoop/common/hadoop-3.1.3/hadoop-3.1.3.tar.gz
cd /opt
tar zxf /tmp/hadoop-3.1.3.tar.gz
ln -s hadoop-3.1.3 hadoop
```

Then proceed to [installation](Installation.md) of TheHive and [configure](Base_configuration.md) everything before starting.

