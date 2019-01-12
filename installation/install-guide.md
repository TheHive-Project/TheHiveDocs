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
RPM packages are published on a Bintray repository. All packages are signed using our GPG key [562CBC1C](https://raw.githubusercontent.com/TheHive-Project/TheHive/master/PGP-PUBLIC-KEY). Its fingerprint is:

`0CD5 AC59 DE5C 5A8E 0EE1  3849 3D99 BB18 562C BC1C`

First install the RPM release package:
```bash
yum install https://dl.bintray.com/thehive-project/rpm-stable/thehive-project-release-1.1.0-2.noarch.rpm
```
This will install TheHive Project's repository in `/etc/yum.repos.d/thehive-rpm.repo` and the corresponding GPG public key in
`/etc/pki/rpm-gpg/GPG-TheHive-Project`.

Then you will able to install the package using `yum`:
```bash
yum install thehive
```

Once the package is installed, proceed to the configuration using the [Configuration Guide](../admin/configuration.md). For additional configuration options, please refer to the [Administration Guide](../admin/admin-guide.md).

#### Pre-release versions
The RPM release package installs two repositories: `thehive-project-stable` and `thehive-project-beta`. The latter contains pre-release, beta versions and is disabled by default. If you want to install them and help us find bugs to the benefit of the whole community, you can enable it by editing `/etc/yum.repos.d/thehive-rpm.repo` and set `enable` value to `1` for `thehive-project-beta` repository.

### DEB
Debian packages are published on a Bintray repository. All packages are signed using our GPG key [562CBC1C](https://raw.githubusercontent.com/TheHive-Project/TheHive/master/PGP-PUBLIC-KEY). Its fingerprint is:

`0CD5 AC59 DE5C 5A8E 0EE1  3849 3D99 BB18 562C BC1C`

To install the x Debian package, use the following commands:
```bash
echo 'deb https://dl.bintray.com/thehive-project/debian-stable any main' | sudo tee -a /etc/apt/sources.list.d/thehive-project.list
sudo apt-key adv --keyserver hkp://pgp.mit.edu --recv-key 562CBC1C
sudo apt-get update
sudo apt-get install thehive
```

Some environments may block access to the `pgp.mit.edu` key server. As a result, the command `sudo apt-key adv --keyserver hkp://pgp.mit.edu --recv-key 562CBC1C` will fail. In that case, you can run the following command instead:

`curl https://raw.githubusercontent.com/TheHive-Project/TheHive/master/PGP-PUBLIC-KEY | sudo apt-key add -`

Once the package is installed, proceed to the configuration using the [Configuration Guide](../admin/configuration.md). For additional configuration options, please refer to the [Administration Guide](../admin/admin-guide.md).

#### Pre-release versions
If you want to install pre-release, beta versions of TheHive packages and help us find bugs to the benefit of the whole community, you can add the pre-release repository with the command:
```bash
echo 'deb https://dl.bintray.com/thehive-project/debian-beta any main' | sudo tee -a /etc/apt/sources.list.d/thehive-project.list
```

### Docker
To use the Docker image, you must use [Docker](https://www.docker.com/) (courtesy of Captain Obvious).

TheHive requires [Elasticsearch](#elasticsearch-inside-a-docker) to run. You can use `docker-compose` to start them together in Docker or install and configure Elasticsearch manually.

#### Use Docker-compose
[Docker-compose](https://docs.docker.com/compose/install/) can start multiple dockers and link them together.

The following [docker-compose.yml](https://raw.githubusercontent.com/TheHive-Project/TheHive/master/docker/thehive/docker-compose.yml)
file starts Elasticsearch and TheHive:
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
    image: thehiveproject/cortex:latest
    depends_on:
      - elasticsearch
    ports:
      - "0.0.0.0:9001:9001"
  thehive:
    image: thehiveproject/thehive:latest
    depends_on:
      - elasticsearch
      - cortex
    ports:
      - "0.0.0.0:9000:9000"
    command: --cortex-port 9001 
```

Put this file in an empty folder and run `docker-compose up`. TheHive is exposed on 9000/tcp port and Cortex on 9001/tcp. These ports can be changed by modifying the `docker-compose` file.

You can specify a custom TheHive configuration file (`application.conf`) by adding the following lines in the `thehive` section of your docker-compose file:

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
Elasticsearch can be installed on the same server as TheHive or on a different one. You can then configure TheHive according to the
[documentation](../admin/admin-guide.md) and run TheHive docker as follow:

```bash
docker run --volume /path/to/thehive/application.conf:/etc/thehive/application.conf thehiveproject/thehive:latest --no-config
```

You can add the `--publish` docker option to expose TheHive HTTP service.

#### Customize the Docker Image
By default, the TheHive Docker image has minimal configuration:
 - choose a random secret (`play.http.secret.key`)
 - search for the Elasticsearch instance (host named `elasticsearch`) and add it to configuration
  - search for a TheHive instance (host named `cortex`) and add it to configuration

This behavior can be disabled by adding `--no-config` to the Docker command line:

`docker run thehiveproject/thehive:latest --no-config`

Or by adding the line `command: --no-config` in the `thehive` section of
docker-compose file.

The image accepts more options:

| Option | Description |
| ------ | ----------- |
| `--no-config` | Do not try to configure TheHive (add the secret and Elasticsearch) |
| `--no-config-secret` | Do not add the random secret to the configuration |
| `--no-config-es` | Do not add the Elasticsearch hosts to configuration |
| `--es-hosts <esconfig>` | Use this string to configure the Elasticsearch hosts (format: `["host1:9300","host2:9300"]`) |
| `--es-hostname <host>` | Resolve this hostname to find Elasticsearch instances |
| `--secret <secret>` | Cryptographic secret needed to secure sessions |
| `--cortex-proto <proto>` | Define the protocol to connect to Cortex (default: `http`) |
| `--cortex-port <port>` | Define the port to connect to Cortex (default: `9001`) |
| `--cortex-url <url>` | Add the Cortex connection |
| `--cortex-hostname <host>` | Resolve this hostname to find the Cortex instance |
| `--cortex-key <key>` | Define Cortex key |

**Note**: please remember that you must **[install and configure Elasticsearch](#elasticsearch-installation)**.

#### What to Do Next?
Once the Docker image is up and running, proceed to the configuration using the [Configuration Guide](../admin/configuration.md). For additional configuration options, please refer to the [Administration Guide](../admin/admin-guide.md).

#### Pre-release Versions
If you would like to use pre-release, beta versions of our Docker images and help us find bugs to the benefit of the whole community, please use `thehiveproject/thehive:version-RCx`. For example `thehiveproject/thehive:3.1.0-RC1`.

### Binary
The following section contains the instructions to manually install TheHive using binaries on **Ubuntu 16.04 LTS**. 

#### 1. Minimal Ubuntu Installation
Install a minimal Ubuntu 16.04 system with the following software:

- Java runtime environment 1.8+ (JRE)
- Elasticsearch 5.x

Make sure your system is up-to-date:

```bash
sudo apt-get update
sudo apt-get upgrade
```

#### 2. Install a Java Virtual Machine
You can install either Oracle Java or OpenJDK.

##### 2.1. Oracle Java
```bash
echo 'deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main' | sudo tee -a /etc/apt/sources.list.d/java.list
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key EEA14886
sudo apt-get update
sudo apt-get install oracle-java8-installer
```

##### 2.2 OpenJDK
```bash
sudo add-apt-repository ppa:openjdk-r/ppa
sudo apt-get update
sudo apt-get install openjdk-8-jre-headless

```

#### 3. Install Elasticsearch
To install Elasticsearch, please read the [Elasticsearch Installation](#elasticsearch-installation) section below.

#### 4. Install TheHive
Binary packages can be downloaded from [Bintray](https://dl.bintray.com/thehive-project/binary/). The latest version is called [thehive-latest.zip](https://dl.bintray.com/thehive-project/binary/thehive-latest.zip).

Download and unzip the chosen binary package. TheHive files can be installed wherever you want on the filesystem. In this guide, we assume you have chosen to install them under `/opt`.

```bash
cd /opt
wget https://dl.bintray.com/thehive-project/binary/thehive-latest.zip
unzip thehive-latest.zip
ln -s thehive-x.x.x thehive
```

**Note**: if you would like to use pre-release, beta versions of and help us find bugs to the benefit of the whole community, please download `https://dl.bintray.com/thehive-project/binary/thehive-version-RCx.zip`. For example `https://dl.bintray.com/thehive-project/binary/thehive-3.1.0-RC1.zip`.

#### 5. First start
It is recommended to use a dedicated, non-privileged user account to start TheHive. If so, make sure that the chosen account can create log files in `/opt/thehive/logs`.

If you'd rather start the application as a service, use the following commands:

```bash
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

```bash
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

```bash
bin/thehive -Dconfig.file=/etc/thehive/application.conf
```

Please note that the service may take some time to start. Once it is started, you may launch your browser and connect to `http://YOUR_SERVER_ADDRESS:9000/`.

Please note that the service may take some time to start.

The first time you connect you will have to create the database schema. Click "Migrate database" to create the DB schema.

![](../images/thehive-first-access_screenshot.png)

Once done, you should be redirected to the page for creating the administrator's account.

![](../images/thehive-admin_account_creation.png)

Once created, you should be redirected to the login page.

![](../images/thehive-login_page.png)

**Warning**: at this stage, if you missed the creation of the admin account, you will not be able to do it unless you
delete TheHive's index from Elasticsearch. In the case you made a mistake, first find out what is the current index of TheHive by running the following command on a host where the Elasticsearch DB used by TheHive is located:

```bash
$ curl http://127.0.0.1:9200/_cat/indices?v
```

The indexes that TheHive uses always start with`the_hive_` following by a number. Let's assume that the output of the command is:

```bash
health status index       uuid                   pri rep docs.count docs.deleted store.size pri.store.size
yellow open   cortex_1    PC_pLFGBS5G2TNQYr4ajgw   5   1        609            6      2.1mb          2.1mb
yellow open   the_hive_13 ft7GGTfhTr-4lSzZw5r1DQ   5   1     180131            3     51.3mb         51.3mb
```

The index used by TheHive is `the_hive_13`. To delete it, run the following command:

```bash
$ curl -X DELETE http://127.0.0.1:9200/the_hive_13
```

Then reload the page or restart TheHive.

#### 6. Update
To update TheHive from binaries, just stop the service, download the latest package, rebuild the link `/opt/thehive` and
restart the service.

```bash
service thehive stop
cd /opt
wget https://dl.bintray.com/thehive-project/binary/thehive-latest.zip
unzip thehive-latest.zip
rm /opt/thehive && ln -s thehive-x.x.x thehive
chown -R thehive:thehive /opt/thehive /opt/thehive-x.x.x
service thehive start
```

#### 7. Configuration
To configure TheHive, read the [Configuration Guide](../admin/configuration.md). For additional configuration options, please refer to the [Administration Guide](../admin/admin-guide.md).

### Build it Yourself
The following section contains a step-by-step guide to build TheHive from its sources.

#### 1. Pre-requisites
The following software are required to download and build TheHive:

* [Java Development Kit 8](http://www.oracle.com/technetwork/java/javase/downloads/index.html) (JDK)
* git: use the system package or [download it](http://www.git-scm.com/downloads)
* [Node.js](https://nodejs.org/en/download/) with its package manager (NPM)
* Grunt: after installing Node.js, run `sudo npm install -g grunt-cli`
* Bower: after installing Node.js, run `sudo npm install -g bower`
* [Elasticsearch 5.6](https://www.elastic.co/downloads/past-releases/elasticsearch-5-6-9)

##### 2. Build
To install the requirements and build TheHive from sources, please follow the instructions below depending on your operating system.

###### 2.1. CentOS/RHEL

**Packages**

```bash
sudo yum -y install git bzip2
```

**Installation of OpenJDK**

```bash
sudo yum -y install java-1.8.0-openjdk-devel
```

**Installation of Node.js**

Install the EPEL repository. You should have the *extras* repository enabled, then: 
 
```bash
sudo yum -y install epel-release
```

Then, you can install Node.js, Grunt, and Bower:

```bash
sudo yum -y install nodejs
sudo npm install -g grunt-cli bower
```

**Installation of Elasticsearch**

To install Elasticsearch, please read the [Elasticsearch Installation](#elasticsearch-installation) section below.

###### 2.2. Ubuntu

**Packages**

```bash
sudo apt-get install git wget
```

**Installation of Oracle JDK**

```bash
echo 'deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main' | sudo tee -a /etc/apt/sources.list.d/java.list
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key EEA14886
sudo apt-get update
sudo apt-get install oracle-java8-installer
```

**Installation of Node.js, Grunt and Bower**

```bash
sudo apt-get install wget
wget -qO- https://deb.nodesource.com/setup_8.x | sudo bash -
sudo apt-get install nodejs
sudo npm install -g grunt-cli bower
```

**Installation of Elasticsearch**

To install Elasticsearch, please read the [Elasticsearch Installation](#elasticsearch-installation) section below.

###### 2.3. TheHive
**Download The Source**

```
git clone https://github.com/TheHive-Project/TheHive.git
```

**Build the Project**

```
cd TheHive
./sbt clean stage
```

This operation may take some time to complete as it will download all dependencies  then build the back-end.
This command cleans previous build files and creates an autonomous package in the `target/universal/stage` directory. This packages contains TheHive binaries with required libraries (`/lib`), configuration files (`/conf`) and startup scripts (`/bin`).

Binaries are built and stored in `TheHive/target/universal/stage/`. You can install them in `/opt/thehive` for example.

```
sudo cp -r TheHive/target/universal/stage /opt/thehive
```

Configure TheHive, read the [Configuration Guide](../admin/configuration.md). For additional configuration options, please refer to the [Administration Guide](../admin/admin-guide.md).

### 2.4 Configure and Start Elasticsearch

Edit `/etc/elasticsearch/elasticsearch.yml` and add the following lines:

```
network.host: 127.0.0.1
script.inline: true
cluster.name: hive
thread_pool.index.queue_size: 100000
thread_pool.search.queue_size: 100000
thread_pool.bulk.queue_size: 1000
```

Start the service:

```
service elasticsearch restart
```

##### 3. First start
Follow the [first start](#4-first-start) section of the binary installation method above to start using TheHive.

##### 4. Build the Front-end Only

Building the back-end builds also the front-end, so you don't need to build it separately. This section is useful only for troubleshooting or for installing the front-end on a reverse proxy.

Go to the front-end directory:
```
cd TheHive/ui
```

Install Node.js libraries, which are required by this step, bower libraries (JavaScript libraries downloaded by the browser). Then
build the front-end :
```
npm install
bower install
grunt build
```

This step generates static files (HTML, JavaScript and related resources) in  the `dist` directory. They can be readily imported on a HTTP server.


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

If Elasticsearch and TheHive run on the same host (and not in a docker), edit `/etc/elasticsearch/elasticsearch.yml` and
set `network.host` parameter with `127.0.0.1`. TheHive use dynamic scripts to make partial updates. Hence, they must be activated using `script.inline: true`.

The cluster name must also be set (`hive` for example). Threadpool queue size must be set with a high value (`100000`). The default size will get the queue easily overloaded.

Edit `/etc/elasticsearch/elasticsearch.yml` and add the following lines:

```
network.host: 127.0.0.1
script.inline: true
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
