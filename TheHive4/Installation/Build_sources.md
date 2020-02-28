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
