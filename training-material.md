## Training Material
TheHive Project maintains a training virtual machine (OVA) containing TheHive, Cortex as well as Cortex analyzers and responders with all their dependencies included, and ElasticSearch. The training VM runs Ubuntu 18.04 with Oracle JRE 8.

The most recent training VM includes:

- TheHive **3.3.1**
- Cortex **2.1.3**
- TheHive4py **1.6.0**
- Cortex4py **2.0.1** 
- and all Cortex analyzers and responders as of **Jun 22, 2019**.

**Warning**: The training VM is solely intended to be used for testing or training purposes. **We strongly encourage you to refrain from using it in production**.

### TL;DR

- Training VM system account : `thehive/thehive1234`
- TheHive URL : http://IP_OF_VM:9000
- Cortex URL : http://IP_OF_VM:9001
- Cortex superAdmin account : `admin/thehive1234`
- Cortex "training" Org admin account  : `thehive/thehive1234` (its key API is used to enable Cortex service in TheHive)

### Get It

You can download the VM from the following location:

[https://drive.google.com/open?id=1v_8GMdXrZnWRiW2X5zw6fXYnCjUD2DPm](https://drive.google.com/open?id=1v_8GMdXrZnWRiW2X5zw6fXYnCjUD2DPm)

To ensure that your download went through nicely, **check the file’s SHA256 hash** which must be equal to the following value:

`d0473d7208af9c7010280cbfa75d4e7d34d971b40f053fff65689d12382cd3f0`

**Note**: On starting the newly imported VM from OVA file in VMware Fusion, you may encounter a message regarding an error with VMWare tools. . By clicking on the `OK` button you would be able to use the VM as expected.

![](images/thehive-vm-vmware-vmwaretools_errormsg.png)

#### Previous Version

The previous version of the training VM is still available for download from the following address:

[https://drive.google.com/open?id=1KXL7kzH7Pc2jSL2o1m1_RwVc3FGw-ixQ](https://drive.google.com/open?id=1KXL7kzH7Pc2jSL2o1m1_RwVc3FGw-ixQ)

To ensure that your download went through nicely, **check the file’s SHA256 hash** which must be equal to the following value:

`387e8a62a82d56fb6fac3f63630733afb98d9c1f4e5f17056d19bc6a82670675`
 
This version includes the following software:

- TheHive **3.2.1**
- Cortex **2.1.3**
- TheHive4py **1.6.0**
- Cortex4py **2.0.1** 
- and all available Cortex analyzers and responders as of **Jan 12, 2019**.

#### Beta Version

We also provide a *beta* training VM containing recent if not the latest release candidates for TheHive, Cortex, TheHive4py and Cortex4py. It contains:
- TheHive **3.4.0-RC2**
- Cortex **3.0.0-RC4**
- TheHive4py **1.6.0**
- Cortex4py **2.0.1** 
- and all available Cortex analyzers and responders as of **July 25, 2019**.

You can download the *beta* training VM from the following location:

[https://drive.google.com/open?id=1y0ZHK_vrcauNFEnrD7N92xxGdbUP9TS1](https://drive.google.com/open?id=1y0ZHK_vrcauNFEnrD7N92xxGdbUP9TS1)

To ensure that your download went through nicely, **check the file’s SHA256 hash** which must be equal to the following value:

`6615de7ab24b8b70b0b895aaecf88e84601f6fab4751069d3923051f3b92e282`

### Use It

To access TheHive, point your browser to the following URL:

[http://IP_OF_VM:9000](http://IP_OF_VM:9000)

To access Cortex, point your browser to the following URL:

[http://IP_OF_VM:(9001)](http://IP_OF_VM:9001)

#### Configure TheHive

The first time you access TheHive, you’ll need to create the associated database by clicking on the `Update Database` button as shown below:

![](images/thehive-first-access_screenshot.png)

TheHive’s configuration file is located in `/etc/thehive/application.conf`. For additional configuration, [read the documentation](README.md).

**Note** : after the first login into TheHive, if the Cortex health check fails (look at the Cortex icon at the bottom right side of the UI), it should success after fully reloading the web page. 

#### Configure Cortex

Cortex is already configured with a superAdmin account `admin/thehive1234`. An organization `training` is also pre-installed with an account `thehive/thehive1234`. This account has `read/analyze/orgAdmin` privileges and TheHive is already configured to use the Cortex service with its key API.

#### Update Analyzers and Use their Report Templates

With the new version, analyzers are disabled by default. The training VM is delivered with _Abuse Finder_, _File_Info_, _Msg_Parser_ and _MaxMind GeoIP_ enabled.

To fully benefit from the latest analyzers, [update them](https://github.com/TheHive-Project/CortexDocs/blob/master/installation/install-guide.md#updating) and install the associated report templates in TheHive:

- [download the report template package](https://dl.bintray.com/thehive-project/binary/report-templates.zip)
- log in TheHive using an administrator account
- go to Admin > Report templates menu
- click on Import templates button and select the downloaded package

#### Plug it with MISP

The test VM does not contain a MISP instance and none is configured in TheHive’s configuration file.  To play with MISP, you may want to [use the VM our good friends at CIRCL provide](https://www.circl.lu/services/misp-training-materials/).  Once you’ve downloaded it or if you have an existing instance, edit `/etc/thehive/application.conf` and [follow the configuration guide](admin/configuration.md#7-misp).

#### Restart or Go Mad

After each modification of `/etc/thehive/application.conf` do not forget to restart the service:

`$ sudo service thehive restart`

After each modification of `/etc/cortex/application.conf` do not forget to restart the service:

`$ sudo service cortex restart`

#### Troubles?

TheHive service logs are located in `/var/log/thehive/application.log`.

Cortex service logs are located in `/var/log/cortex/application.log`.

#### Need Help?

Something does not work as expected? No worries, we got you covered. Please join our  [user forum](https://groups.google.com/a/thehive-project.org/forum/#!forum/users), contact us on [Gitter](https://gitter.im/TheHive-Project/TheHive), or send us an email at [support@thehive-project.org](mailto:support@thehive-project.org). We are here to help.
