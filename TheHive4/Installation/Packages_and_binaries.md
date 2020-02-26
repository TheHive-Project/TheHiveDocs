# Packages and binaries

## Using DEB package

Debian packages are published on a our DEB packages repository. All packages are signed using our GPG key [562CBC1C](https://raw.githubusercontent.com/TheHive-Project/TheHive/master/PGP-PUBLIC-KEY). Its fingerprint is:

`0CD5 AC59 DE5C 5A8E 0EE1  3849 3D99 BB18 562C BC1C`

Some environments may block access to the `pgp.mit.edu` key server. As a result, the command `sudo apt-key adv --keyserver hkp://pgp.mit.edu --recv-key 562CBC1C` will fail. In that case, you can run the following command instead:

`curl https://raw.githubusercontent.com/TheHive-Project/TheHive/master/PGP-PUBLIC-KEY | sudo apt-key add -`


To install the  Debian package, use the following commands:
```bash
echo 'deb https://deb.thehive-project.org beta main' | sudo tee -a /etc/apt/sources.list.d/thehive-project.list
sudo apt-key adv --keyserver hkp://pgp.mit.edu --recv-key 562CBC1C
sudo apt-get update
sudo apt-get install thehive
```

Once the package is installed, proceed to the configuration using the [Configuration Guide](Base_configuration.md). For additional configuration options, please refer to the [Administration Guide](/admin/admin-guide.md).

## Using RPM package

RPM packages are published on a our RPM repository. All packages are signed using our GPG key [562CBC1C](https://raw.githubusercontent.com/TheHive-Project/TheHive/master/PGP-PUBLIC-KEY). Its fingerprint is:

`0CD5 AC59 DE5C 5A8E 0EE1  3849 3D99 BB18 562C BC1C`

First setup your system to connect the RPM repository. Create and edit the file `/etc/yum.repo.d/thehive-project.repo`: 
```bash
[thehive-project]
enabled=1
priority=1
name=TheHive-Project RPM repository
baseurl=http://rpm.thehive-project.org/beta/noarch
gpgcheck=1
```
Then run the following command to import the GPG key :

```bash
sudo rpm --import https://raw.githubusercontent.com/TheHive-Project/TheHive/master/PGP-PUBLIC-KEY
```

Then you will able to install the package using `yum`:
```bash
yum install thehive
```

Once the package is installed, proceed to the configuration using the [Configuration Guide](base_configuration.md). For additional configuration options, please refer to the [Administration Guide](../Administration/README.md).



## Using binaries



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
cd TheHive
git checkout scalligraph
git submodule init
git submodule update
./sbt stage
```

- The UI

```bash
cd /opt/TheHive/frontend
npm install
bower install
grunt build
```
