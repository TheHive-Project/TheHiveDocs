# Installing TheHive Using an RPM Package

TheHive's RPM packages are published on our Bintray repository. All packages are PGP signed using the key which ID is [562CBC1C](/PGP-PUBLIC-KEY). The key's fingerprint is:

```0CD5 AC59 DE5C 5A8E 0EE1  3849 3D99 BB18 562C BC1C```

To intall TheHive from an RPM package, you'll need to begin by installing the RPM release package using the following command:
```
yum install https://dl.bintray.com/cert-bdf/rpm/thehive-project-release-1.0.0-3.noarch.rpm
```
This will install TheHive Project's repository in `/etc/yum.repos.d/thehive-rpm.repo` and the GPG public key `in
/etc/pki/rpm-gpg/GPG-TheHive-Project`.
 
Once done, you will able to install TheHive package using yum:
```
yum install thehive
```

One installed, you should [install ElasticSearch](elasticsearch-guide.md) and [configure TheHive](../admin/configuration.md).

## Turnkey RPM Installation
In the event that you need a turnkey installation of TheHive (including Cortex), this will work with RHEL/CentOS 7.3+:
```
#!/bin/bash

################################
######### Epel Release #########
################################
# The DISA STIG for CentOS 7.4.1708 enforces a GPG signature check for all repodata. While this is generally a good idea, it causes repos tha do not use GPG Armor to fail.
# One example of a repo that does not use GPG Armor is Epel; which is a dependency of CAPES (and tons of other projects, for that matter).
# To fix this, we are going to disable the GPG signature and local RPM GPG signature checking.
# I'm open to other options here.
# RHEL's official statement on this: https://access.redhat.com/solutions/2850911
sudo sed -i 's/repo_gpgcheck=1/repo_gpgcheck=0/' /etc/yum.conf
sudo sed -i 's/localpkg_gpgcheck=1/localpkg_gpgcheck=0/' /etc/yum.conf

# Set your IP address as a variable. This is for instructions below.
IP="$(hostname -I | sed -e 's/[[:space:]]*$//')"

################################
########### TheHive ############
################################

# Dependencies
sudo yum install java-1.8.0-openjdk.x86_64 epel-release -y && sudo yum update -y
sudo yum groupinstall "Development Tools" -y
sudo rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
sudo yum install https://kojipkgs.fedoraproject.org/packages/http-parser/2.7.1/3.el7/x86_64/http-parser-2.7.1-3.el7.x86_64.rpm libffi-devel python-devel python-pip ssdeep-devel ssdeep-libs perl-Image-ExifTool file-devel https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.6.0.rpm -y

# Configure Elasticsearch
sudo bash -c 'cat > /etc/elasticsearch/elasticsearch.yml <<EOF
network.host: 127.0.0.1
cluster.name: hive
script.inline: true
thread_pool.index.queue_size: 100000
thread_pool.search.queue_size: 100000
thread_pool.bulk.queue_size: 1000
EOF'

# Collect the Cortex analyzers
sudo git clone https://github.com/CERT-BDF/Cortex-Analyzers.git /opt/cortex/

# Collect the Cortex Report Templates
sudo curl -L https://dl.bintray.com/cert-bdf/thehive/report-templates.zip -o /opt/cortex/report-templates.zip

# Install TheHive Project and Cortex
# TheHive Project is the incident tracker, Cortex is your analysis engine.
# If you're going to be using this offline, you can remove the Cortex install (sudo yum install thehive -y).
sudo rpm --import https://dl.bintray.com/cert-bdf/rpm/repodata/repomd.xml.key
sudo yum install https://dl.bintray.com/cert-bdf/rpm/thehive-project-release-1.0.0-3.noarch.rpm -y
sudo yum install thehive cortex -y

# Configure TheHive Project secret key
(cat << _EOF_
# Secret key
# ~~~~~
# The secret key is used to secure cryptographics functions.
# If you deploy your application to several instances be sure to use the same key!
play.crypto.secret="$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1)"
_EOF_
) | sudo tee -a /etc/thehive/application.conf

# Configure Cortex secret key
(cat << _EOF_
# Secret key
# ~~~~~
# The secret key is used to secure cryptographics functions.
# If you deploy your application to several instances be sure to use the same key!
play.crypto.secret="$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1)"
_EOF_
) | sudo tee -a /etc/cortex/application.conf

# Make firewall changes to allow for access to TheHive Project and Cortex web applications
sudo firewall-cmd --add-port=9000/tcp --add-port=9001/tcp --permanent
sudo firewall-cmd --reload

# Update Pip...just because it's ludicious that installing it doesn't bring the updated version
sudo pip install --upgrade pip
# Add the future Python package and then install the Cortex Python dependencies
sudo pip install future
# for d in /opt/cortex/analyzers/*/ ; do (sudo pip install -r $d/requirements.txt); done

for d in /opt/cortex/analyzers/*/ ; do (cat $d/requirements.txt >> requirements.staged); done
sort requirements.staged | uniq > requirements.txt
rm requirements.staged
sudo pip install -r requirements.txt
rm requirements.txt

# Update the location of the analyzers
sudo sed -i 's/path\/to\/Cortex\-Analyzers/\/opt\/cortex/' /etc/cortex/application.conf

# Ensure that thehive and cortex users owns it's directories
sudo chown -R thehive:thehive /opt/thehive
sudo chown thehive:thehive /etc/thehive/application.conf
sudo chmod 640 /etc/thehive/application.conf
sudo chown -R cortex:cortex /opt/cortex
sudo chown cortex:cortex /etc/cortex/application.conf
sudo chmod 640 /etc/cortex/application.conf

# Configure Cortex to run on port 9001 instead of the default 9000, which is shared with TheHive
sudo sed -i '16i\\t-Dhttp.port=9001 \\' /etc/systemd/system/cortex.service
sudo systemctl daemon-reload

# Connect TheHive to Cortex
sudo bash -c 'cat >> /etc/thehive/application.conf <<EOF
# Cortex
play.modules.enabled += connectors.cortex.CortexConnector
cortex {
  "CORTEX-SERVER-ID" {
  url = "http://$HOSTNAME:9001"
  }
}
EOF'

# Set Elasticsearch and TheHive Project to start on boot
sudo systemctl enable elasticsearch.service
sudo systemctl enable thehive.service
sudo systemctl enable cortex.service

# Start TheHive, Elasticsearch, and Cortex
sudo systemctl start elasticsearch.service
sudo systemctl start cortex.service
sudo systemctl start thehive.service

# Success
clear
cat << "EOF"


               `          `
             ``   `    `   ``
            ``     ````     ``
           ``      ....      ``
           ``       ``       ``
            ``   ```  ```   ``
              ``..` `` `..``
             `...` ```` `...`
            .....        .....
            ````  ``````  ````
                  ``````
                   ````
EOF
echo "TheHive has been successfully deployed. Browse to http://$HOSTNAME:9000 (or http://$IP:9000 if you don't have DNS set up) to begin using the service.
"
echo "Cortex has been successfully deployed. Browse to http://$HOSTNAME:9001 (or http://$IP:9001 if you don't have DNS set up) to begin using the service.
"
```
