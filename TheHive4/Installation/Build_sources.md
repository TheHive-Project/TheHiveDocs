## Installing and running from sources

### Dependencies

#### System packages

```bash
apt-get install apt-transport-https
```

#### NPM

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.0/install.sh | bash
```

#### Bower and Grunt

```bash
nvm install --lts
npm install -g bower grunt
```

### Build

- The backend

```bash
cd /opt
git clone https://github.com/TheHive-Project/TheHive.git
cd TheHive
git checkout master-th4
git submodule init
git submodule update
./sbt stage
```
To start the backend in dev mode instead 
```bash
 ./sbt stage
 ```
 do :
```bash
./sbt run
```
- The UI

```bash
cd /opt/TheHive/frontend
npm install
bower install
grunt build
```
To start the frontend:
```bash
 grunt serve
```

### Creating deb package on Ubuntu 20.04

```bash
sudo apt install default-jre 
sudo apt install apt-transport-https
sudo apt install fakeroot
sudo apt install curl
sudo apt install git
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.0/install.sh | bash
```
Open a new terminal
```bash
nvm install --lts
npm install -g bower grunt
```
```
git clone https://github.com/TheHive-Project/TheHive.git
cd TheHive
git checkout master-th4
git submodule init
git submodule update
```
```
./sbt clean debian:packageBin
```
After a while you will get something like
```
[info] Building debian package with native implementation
[info] dpkg-deb: building package 'thehive4' in '../thehive4_4.0.2-1_all.deb'.
[success] Total time: 1032 s (17:12), completed Dec 11, 2020, 10:45:45 AM
```
The deb package is located under target folder
```
user@user:~/TheHive$ ls -la target
total 185744
drwxrwxr-x  8 user user      4096 Dec 11 10:45 .
drwxrwxr-x 22 user user      4096 Dec 11 10:00 ..
drwxrwxr-x  2 user user      4096 Dec 11 10:45 global-logging
drwxrwxr-x  6 user user      4096 Dec 11 10:37 scala-2.12
drwxrwxr-x  7 user user      4096 Dec 11 10:25 streams
drwxrwxr-x  2 user user      4096 Dec 11 10:45 task-temp-directory
drwxrwxr-x  7 user user      4096 Dec 11 10:25 thehive4-4.0.2-1
-rw-r--r--  1 user user 190167232 Dec 11 10:45 thehive4_4.0.2-1_all.deb
drwxrwxr-x  4 user user      4096 Dec 11 10:24 universal
```
So can install with:
```
sudo dpkg -i target/thehive4_4.0.2-1_all.deb
```
Ensure to follow the [deb guide](https://github.com/TheHive-Project/TheHiveDocs/blob/master/TheHive4/Installation/Install_deb.md) before install this package.