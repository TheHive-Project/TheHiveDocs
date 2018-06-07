# Installation Guide
Before installing TheHive, you need to choose the installation option which suits your environment as described below. Once you have a chosen an option and installed the software, read the [Configuration Guide](../admin/configuration.md). We also advise reading the [Administration Guide](../admin/admin-guide.md).

## Table of Contents
  * [Installation Options](#installation-options)
    * [RPM](#rpm)
    * [DEB](#deb)
    * [Docker](#docker)
    * [Binary](#binary)
    * [Build it Yourself](#build-it-yourself)
  * [Elasticsearch Installation](#elasticsearch-installation)
    * [System Package](#system-package)
    * [Start the Service](#start-the-service)
    * [Elasticsearch inside a Docker](#elasticsearch-inside-a-docker)

## Installation Options
TheHive is available as:

- an [RPM package](#rpm)
- a [DEB package](#deb)
- a [Docker image](#docker)
- a [binary package](#binary)

In addition, TheHive can be also be [built from the source code](#build-it-yourself).

### RPM
RPM packages are published on a Bintray repository. All packages are signed using our GPG key [562CBC1C](https://raw.githubusercontent.com/TheHive-Project/Cortex/master/PGP-PUBLIC-KEY). Its fingerprint is:

`0CD5 AC59 DE5C 5A8E 0EE1  3849 3D99 BB18 562C BC1C`

First install the RPM release package:
```
yum install https://dl.bintray.com/cert-bdf/rpm/thehive-project-release-1.0.0-3.noarch.rpm
```
This will install TheHive Project's repository in `/etc/yum.repos.d/thehive-rpm.repo` and the corresponding GPG public key in
`/etc/pki/rpm-gpg/GPG-TheHive-Project`.

Then you will able to install the package using `yum`:
```
yum install thehive
```

Once the package is installed, proceed to the configuration using the [Configuration Guide](../admin/configuration.md). For additional configuration options, please refer to the [Administration Guide](../admin/admin-guide.md).

### DEB
Debian packages are published on a Bintray repository. All packages are signed using our GPG key [562CBC1C](https://raw.githubusercontent.com/TheHive-Project/Cortex/master/PGP-PUBLIC-KEY). Its fingerprint is:

`0CD5 AC59 DE5C 5A8E 0EE1  3849 3D99 BB18 562C BC1C`

To install the Cortex Debian package, use the following commands:
```
echo 'deb https://dl.bintray.com/cert-bdf/debian any main' | sudo tee -a /etc/apt/sources.list.d/thehive-project.list
sudo apt-key adv --keyserver hkp://pgp.mit.edu --recv-key 562CBC1C
sudo apt-get update
sudo apt-get install thehive
```

Some environments may block access to the `pgp.mit.edu` key server. As a result, the command `sudo apt-key adv --keyserver hkp://pgp.mit.edu --recv-key 562CBC1C` will fail. In that case, you can run the following command instead:

`curl https://raw.githubusercontent.com/TheHive-Project/Cortex/master/PGP-PUBLIC-KEY | sudo apt-key add -`

Once the package is installed, proceed to the configuration using the [Configuration Guide](../admin/configuration.md). For additional configuration options, please refer to the [Administration Guide](../admin/admin-guide.md).

### Docker
To use the Docker image, you must use [Docker](https://www.docker.com/) (courtesy of Captain Obvious).

TheHive requires [Elasticsearch](#elasticsearch-inside-a-docker) to run. You can use `docker-compose` to start them together in Docker or install and configure Elasticsearch manually.

#### Use Docker-compose
[Docker-compose](https://docs.docker.com/compose/install/) can start multiple dockers and link them together.

The following [docker-compose.yml](https://raw.githubusercontent.com/TheHive-Project/TheHive/master/docker/cortex/docker-compose.yml)
file starts Elasticsearch and Cortex:
```
version: "2"
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:5.6.0
    environment:
      - http.host=0.0.0.0
      - transport.host=0.0.0.0
      - xpack.security.enabled=false
      - cluster.name=hive
      - script.inline=true
      - thread_pool.index.queue_size=100000
      - thread_pool.search.queue_size=100000
      - thread_pool.bulk.queue_size=100000
    ulimits:
      nofile:
        soft: 65536
        hard: 65536
  cortex:
    image: certbdf/cortex:latest
    ports:
      - "0.0.0.0:9001:9000"
  thehive:
    image: certbdf/thehive:latest
    depends_on:
      - elasticsearch
      - cortex
    ports:
      - "0.0.0.0:9000:9000"
```

Put this file in an empty folder and run `docker-compose up`. TheHive is exposed on 9000/tcp port and Cortex on 9001/tcp. These ports can be changed by modifying the `docker-compose` file.

You can specify a custom TheHive configuration file (`application.conf`) by adding the following lines in the `cortex` section of your docker-compose file:

```
volumes:
    - /path/to/application.conf:/etc/thehive/application.conf
```

You should define where the data (i.e. the Elasticsearch database) will be located on your operating system by adding the following lines in the `elasticsearch` section of your docker-compose file:
```
volumes:
    - /path/to/data:/usr/share/elasticsearch/data
```

Running ElasticSearch in production mode requires a minimum `vm.max_map_count` of 262144. [ElasticSearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#docker-cli-run-prod-mode) provides instructions on how to query and change this value.

#### Manual Installation of Elasticsearch
Elasticsearch can be installed on the same server as Cortex or on a different one. You can then configure Cortex according to the
[documentation](../admin/admin-guide.md) and run Cortex docker as follow:

```
docker run --volume /path/to/thehive/application.conf:/etc/thehive/application.conf certbdf/thehive:latest --no-config
```

You can add the `--publish` docker option to expose TheHive HTTP service.

#### Customize the Docker Image
By default, the Cortex Docker image has minimal configuration:
 - choose a random secret (`play.http.secret.key`)
 - search for the Elasticsearch instance (host named `elasticsearch`) and add it to configuration
  - search for a Cortex instance (host named `cortex`) and add it to configuration

This behavior can be disabled by adding `--no-config` to the Docker command line:

`docker run certbdf/thehive:latest --no-config`

Or by adding the line `command: --no-config` in the `cortex` section of
docker-compose file.

The image accepts more options:

| Option | Description |
| ------ | ----------- |
| `--no-config` | Do not try to configure Cortex (add the secret and Elasticsearch) |
| `--no-config-secret` | Do not add the random secret to the configuration |
| `--no-config-es` | Do not add the Elasticsearch hosts to configuration |
| `--es-hosts <esconfig>` | Use this string to configure the Elasticsearch hosts (format: `["host1:9300","host2:9300"]`) |
| `--es-hostname <host>` | Resolve this hostname to find Elasticsearch instances |
| `--secret <secret>` | Cryptographic secret needed to secure sessions |
| `--cortex-proto <proto>` | Define the protocol to connect to Cortex (default: `http`) |
| `--cortex-port <port>` | Define the port to connect to Cortex (default: `9001`) |
| `--cortex-url <url>` | Add the Cortex connection |
| `cortex-hostname <host>` | Resolve this hostname to find the Cortex instance |

**Note**: please remember that you must **[install and configure Elasticsearch](#elasticsearch-installation)**.

#### What to Do Next?
Once the Docker image is up and running, proceed to the configuration using the [Configuration Guide](../admin/configuration.md). For additional configuration options, please refer to the [Administration Guide](../admin/admin-guide.md).

### Binary
The following section contains the instructions to manually install TheHive using binaries on **Ubuntu 16.04 LTS**. 

#### 1. Minimal Ubuntu Installation
Install a minimal Ubuntu 16.04 system with the following software:

- Java runtime environment 1.8+ (JRE)
- Elasticsearch 5.x

Make sure your system is up-to-date:

```
sudo apt-get update
sudo apt-get upgrade
```

#### 2. Install a Java Virtual Machine
You can install either Oracle Java or OpenJDK.

##### 2.1. Oracle Java
```
echo 'deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main' | sudo tee -a /etc/apt/sources.list.d/java.list
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key EEA14886
sudo apt-get update
sudo apt-get install oracle-java8-installer
```

##### 2.2 OpenJDK
```
sudo add-apt-repository ppa:openjdk-r/ppa
sudo apt-get update
sudo apt-get install openjdk-8-jre-headless

```

#### 3. Install Elasticsearch
To install Elasticsearch, please read the [Elasticsearch Installation](#elasticsearch-installation) section below.

#### 4. Install TheHive
Binary packages can be downloaded from [Bintray](https://dl.bintray.com/cert-bdf/thehive/). The latest version is called [thehive-latest.zip](https://dl.bintray.com/cert-bdf/thehive/thehive-latest.zip).

Download and unzip the chosen binary package. Cortex files can be installed wherever you want on the filesystem. In this guide, we assume you have chosen to install them under `/opt`.

```
cd /opt
wget https://dl.bintray.com/cert-bdf/cortex/thehive-latest.zip
unzip thehive-latest.zip
ln -s thehive-x.x.x thehive
```

#### 4. First start
It is recommended to use a dedicated, non-privileged user account to start TheHive. If so, make sure that the chosen account can create log files in `/opt/thehive/logs`.

If you'd rather start the application as a service, use the following commands:
```
sudo addgroup thehive
sudo adduser --system thehive
sudo cp /opt/thehive/package/thehive.service /usr/lib/systemd/system
sudo chown -R thehive:thehive /opt/thehive
sudo chgrp thehive /etc/thehive/application.conf
sudo chmod 640 /etc/thehive/application.conf
sudo systemctl enable thehive
sudo service thehive start
```

The only required parameter in order to start TheHive is the key of the server (`play.http.secret.key`). This key is used
to authenticate cookies that contain data. If TheHive runs in cluster mode, all instances must share the same key.
You can generate the minimal configuration with the following commands (they assume that you have created a
dedicated user for TheHive, named `thehive`):

```
sudo mkdir /etc/thehive
(cat << _EOF_
# Secret key
# ~~~~~
# The secret key is used to secure cryptographics functions.
# If you deploy your application to several instances be sure to use the same key!
play.http.secret.key="$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1)"
_EOF_
) | sudo tee -a /etc/thehive/application.conf
```

Now you can start TheHive. To do so, change your current directory to the TheHive installation directory (`/opt/thehive` in this guide), then execute:

```
bin/thehive -Dconfig.file=/etc/thehive/application.conf
```

Please note that the service may take some time to start. Once it is started, you may launch your browser and connect to `http://YOUR_SERVER_ADDRESS:9000/`.

#### 6. Update
To update TheHive from binaries, just stop the service, download the latest package, rebuild the link `/opt/thehive` and
restart the service.

```
service thehive stop
cd /opt
wget https://dl.bintray.com/cert-bdf/cortex/thehive-latest.zip
unzip thehive-latest.zip
rm /opt/thehive && ln -s thehive-x.x.x thehive
chown -R thehive:thehive /opt/thehive /opt/thehive-x.x.x
service thehive start
```

#### 7. Configuration
To configure TheHive, read the [Configuration Guide](../admin/configuration.md). For additional configuration options, please refer to the [Administration Guide](../admin/admin-guide.md).

### Build it Yourself
The following section contains a step-by-step guide to build Cortex from its sources.

#### 1. Pre-requisites
The following software are required to download and build Cortex:

* [Java Development Kit 8](http://www.oracle.com/technetwork/java/javase/downloads/index.html) (JDK)
* git: use the system package or [download it](http://www.git-scm.com/downloads)
* [Node.js](https://nodejs.org/en/download/) with its package manager (NPM)

##### 2. Build
To install the requirements and build Cortex from sources, please follow the instructions below depending on your operating system.

###### 2.1. CentOS/RHEL

**Packages**

```
sudo yum -y install git bzip2
```

**Installation of OpenJDK**

```
sudo yum -y install java-1.8.0-openjdk-devel
```

**Installation of Node.js**

Install the EPEL repository. You should have the *extras* repository enabled, then:  
```
sudo yum -y install epel-release
```

Then, you can install Node.js:

```
sudo yum -y install nodejs
```

###### 2.2. Ubuntu

**Packages**

```
sudo apt-get install git wget
```

**Installation of Oracle JDK**

```
echo 'deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main' | sudo tee -a /etc/apt/sources.list.d/java.list
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key EEA14886
sudo apt-get update
sudo apt-get install oracle-java8-installer
```

**Installation of Node.js**

```
sudo apt-get install wget
wget -qO- https://deb.nodesource.com/setup_8.x | sudo bash -
sudo apt-get install nodejs
```

###### 2.3. Cortex
**Download The Source**

```
git clone https://github.com/CERT-BDF/Cortex.git
```

**Build the Project**

```
cd Cortex
./sbt clean stage
```

This operation may take as it will download all dependencies then build the back-end.
This command cleans any previous build files and create an autonomous package under the `target/universal/stage` directory. This package contains Cortex binaries with the required libraries (`/lib`), configuration files (`/conf`) and startup scripts (`/bin`).

Binaries are built and stored under `Cortex/target/universal/stage/`. You caniInstall them for example in `/opt/cortex`.

```
sudo cp -r Cortex/target/universal/stage /opt/cortex
```

Proceed to [installing the analyzers](#analyzers-1) as outlined in the next section and configure Cortex using the [Quick Start Guide](../admin/quick-start.md). For more advanced configuration options, please refer to the [Administration Guide](../admin/admin-guide.md).

##### 3. First start
Follow the [first start](#4-first-start) section of the binary installation method above to start using Cortex.

##### 4. Build the Front-end Only
Building the back-end builds also the front-end, so you don't need to build it separately. This section is useful only for troubleshooting or for installing the front-end on a reverse proxy.

Go to the front-end directory:
```
cd Cortex/www
```

Install Node.js libraries, which are required by this step, bower libraries (JavaScript libraries downloaded by the browser). Then
build the front-end :
```
npm install
npm run build
```

This step generates static files (HTML, JavaScript and related resources) in  the `dist` directory. They can be readily imported on a HTTP server.

## Analyzers
Analyzers are autonomous applications managed by and run through the Cortex core engine. Analyzers have their
[own dedicated GitHub repository](https://github.com/TheHive-Project/Cortex-Analyzers). 
They are included in the Cortex binary, RPM and DEB packages and in the Docker image as well. However, you to get them from the repository if you need to update them after installing one of those packages. This operation is is necessary when new analyzers are released or new versions of existing ones are made available, or if you decide to build Cortex from sources.

### Installation
Currently, all the analyzers supported by TheHive Project are written in Python 2 or 3. They don't require any build phase but their dependencies have
to be installed. Before proceeding, you'll need to install the system package dependencies that are required by some of them:

```
sudo apt-get install -y --no-install-recommends python-pip python2.7-dev python3-pip python3-dev ssdeep libfuzzy-dev libfuzzy2 libimage-exiftool-perl libmagic1 build-essential git libssl-dev
```

You may need to install Python's `setuptools` and update pip/pip3:
```
sudo pip install -U pip setuptools && sudo pip3 install -U pip setuptools
```

Once finished, clone the Cortex-analyzers repository in the directory of your choosing:
```
git clone https://github.com/TheHive-Project/Cortex-Analyzers

```

Each analyzer comes with its own, pip compatible `requirements.txt` file. You can install all requirements with the following commands:

```
for I in Cortex-Analyzers/analyzers/*/requirements.txt; do sudo -H pip2 install -r $I; done && \
for I in Cortex-Analyzers/analyzers/*/requirements.txt; do sudo -H pip3 install -r $I || true; done
```

Next, you'll need to tell Cortex where to find the analyzers. Analyzers may be in different directories as shown in this dummy example of the Cortex configuration file (`application.conf`):

```
analyzer {
  # Directory that holds analyzers
  path = [
    "/path/to/default/analyzers",
    "/path/to/my/own/analyzers"
  ]

  fork-join-executor {
    # Min number of threads available for analyze
    parallelism-min = 2
    # Parallelism (threads) ... ceil(available processors * factor)
    parallelism-factor = 2.0
    # Max number of threads available for analyze
    parallelism-max = 4
  }
}
```
### Configuration
All analyzers must be configured using the Web UI. Please read the [Quick Start Guide](../admin/quick-start.md) to create at least one organization then let a user with the `orgAdmin` role configure and enable analyzers for that organization.

Some analyzers can be used out of the box, without any configuration, while others may require various parameters. Please check the [Analyzer Requirements Guide](../analyzer_requirements.md) for further details.

### Updating
Existing Cortex analyzers are regularly updated and new ones are added. To benefit from the latest bug fixes, enhancements and additions, run the following commands:

```bash
$ cd /path/to/Cortex-Analyzers
$ sudo git pull
```
Then install any missing requirements:

```bash
for I in /path/to/Cortex-Analyzers/analyzers/*/requirements.txt; do sudo -H pip2 install -r $I; done && \
for I in /path/to/Cortex-Analyzers/analyzers/*/requirements.txt; do sudo -H pip3 install -r $I || true; done
```
After running these commands, read the Analyzer Requirements Guide,  log into the Cortex 2 Web UI as an `orgAdmin`, click on the Refresh Analyzers button in the Cortex Web UI, configure the new analyzers and enjoy!

If you are using TheHive, get the [latest version of the report templates](https://dl.bintray.com/cert-bdf/thehive/report-templates.zip) and import them into TheHive.

### Additional Analyzers
The following analyzers are not supported by THeHive Project at this time:

- [Analyzers written in Go](https://github.com/Rostelecom-CERT/go-cortex-analyzers) by Rosetelecom-CERT

## Elasticsearch Installation
If, for some reason, you need to install Elasticsearch, it can be installed using a system package or a Docker image. The latter is preferred as its installation and update are easier.

### System Package
Install the Elasticsearch package provided by Elastic:
```
# PGP key installation
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key D88E42B4

# Alternative PGP key installation
# wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -

# Debian repository configuration
echo "deb https://artifacts.elastic.co/packages/5.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-5.x.list

# Install https support for apt
sudo apt install apt-transport-https

# Elasticsearch installation
sudo apt update && sudo apt install elasticsearch
```

The Debian package does not start up the service by default,  to prevent the instance from accidentally joining a cluster, without being configured appropriately.

If you prefer using Elasticsearch inside a docker, see
[Elasticsearch inside a Docker](#elasticsearch-inside-a-docker).

#### Configuration
It is **highly recommended** to avoid exposing this service to an untrusted zone.

If Elasticsearch and Cortex run on the same host (and not in a docker), edit `/etc/elasticsearch/elasticsearch.yml` and
set `network.host` parameter with `127.0.0.1`. Cortex use dynamic scripts to make partial updates. Hence, they must be activated using `script.inline: on`.

The cluster name must also be set (`hive` for example). Threadpool queue size must be set with a high value (`100000`). The default size will get the queue easily overloaded.

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
Now that Elasticsearch is configured, start it as a service and check whether it's running:
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

### Elasticsearch inside a Docker
You can also start Elasticsearch inside a docker. Use the following command and do not forget to specify the absolute path for persistent data on your host :

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
	docker.elastic.co/elasticsearch/elasticsearch:5.6.0
```