## Training Material
TheHive Project maintains training virtual machines (OVA) containing TheHive, Cortex as well as Cortex analyzers and responders: 

**Stable versions:**

- [TheHive 4.0.0](#thehive-40)
- [TheHive 3.4.0](#thehive-340)

**Beta versions:**

- [TheHive 3.4.0-RC2](#beta-version)


**Warning**: The training VMs are solely intended to be used for testing or training purposes. **We strongly encourage you to refrain from using it in production**.


### TheHive 4.0

The training VM runs Ubuntu 20.04 with OpenJDK JRE 8.
The most recent training VM includes:

- TheHive **4.0.0-1** using a local BerkeleyDB and file storage, 
- Cortex **3.0.1**, and Elasticsearch **6.8**.
- TheHive4py **1.7.2**
- Cortex4py **2.0.1** 
- Cortex Analyzers and Responders running with Docker 

#### Accounts and credentials

- Training VM system account (ssh) : `thehive/thehive1234`
- TheHive URL : http://IP_OF_VM:9000
- TheHive superAdmin account: `admin/secret` or `admin@thehive.local/secret` 
- Cortex URL : http://IP_OF_VM:9001
- Cortex superAdmin account : `admin/thehive1234`
- Cortex "training" Org admin account  : `thehive/thehive1234` (its key API is used to enable Cortex service in TheHive)

#### Download information

You can download the VM from the following location:

[https://download.thehive-project.org/thehive-training-4.0.ova](https://download.thehive-project.org/thehive-training-4.0.ova)

To ensure that your download went through nicely, **check the file’s SHA256 hash** which must be equal to the following value:

`530639b1c4793216ed025063dc79806607884be00e8a1bcd6fc643751d84e7ed`

### TheHive 3.4.0

TheHive Project maintains a training virtual machine (OVA) containing TheHive, Cortex as well as Cortex analyzers and responders with all their dependencies included, and ElasticSearch. The training VM runs Ubuntu 18.04 with Oracle JRE 8.

The most recent training VM includes:

- TheHive **3.4.0**
- Cortex **3.0.1**
- TheHive4py **1.6.0**
- Cortex4py **2.0.1** 
- and all Cortex analyzers and responders as of **Jan 29, 2019**.

**Warning**: The training VM is solely intended to be used for testing or training purposes. **We strongly encourage you to refrain from using it in production**.

#### Accounts and credentials

- Training VM system account (ssh) : `thehive/thehive1234`
- TheHive URL : http://IP_OF_VM:9000
- TheHive Admin account: `admin/thehive1234`
- Cortex URL : http://IP_OF_VM:9001
- Cortex superAdmin account : `admin/thehive1234`
- Cortex "training" Org admin account  : `thehive/thehive1234` (its key API is used to enable Cortex service in TheHive)

#### Download information

You can download the VM from the following location:

[https://drive.google.com/open?id=1TzuWkK8POrUvXoVPwKmA_NQFL02wctz_](https://drive.google.com/open?id=1TzuWkK8POrUvXoVPwKmA_NQFL02wctz_)

To ensure that your download went through nicely, **check the file’s SHA256 hash** which must be equal to the following value:

`b6dd44634421475a82aaa642ad562e48d24291c996c27fafd8761d85de87d9fe`

**Note**: On starting the newly imported VM from OVA file in VMware Fusion, you may encounter a message regarding an error with VMWare tools. . By clicking on the `OK` button you would be able to use the VM as expected.

![](images/thehive-vm-vmware-vmwaretools_errormsg.png)

#### Previous Version

The previous version of the training VM is still available for download from the following address:

[https://drive.google.com/open?id=1v_8GMdXrZnWRiW2X5zw6fXYnCjUD2DPm](https://drive.google.com/open?id=1v_8GMdXrZnWRiW2X5zw6fXYnCjUD2DPm)

To ensure that your download went through nicely, **check the file’s SHA256 hash** which must be equal to the following value:

`d0473d7208af9c7010280cbfa75d4e7d34d971b40f053fff65689d12382cd3f0`

This version includes the following software:

- TheHive **3.3.1**
- Cortex **2.1.3**
- TheHive4py **1.6.0**
- Cortex4py **2.0.1** 
- and all available Cortex analyzers and responders as of **Jun 22, 2019**.

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

TheHive is already configured and comes with a default superAdmin account:

- `admin/thehive1234` for TheHive 3.x versions
- `admin/secret` or `admin@thehive.local/secret` for thehive 4.x versions

**Note** : after the first login into TheHive, if the Cortex health check fails (look at the Cortex icon at the bottom right side of the UI), it should success after fully reloading the web page. 

#### Configure Cortex

Cortex is already configured with a superAdmin account `admin/thehive1234`.
An organization `training` is also pre-installed with an account `thehive/thehive1234`. This account has `read/analyze/orgAdmin` privileges and TheHive is already configured to use the Cortex service with its key API.

####  Analyzers, Responders and their Report Templates

TheHive and Cortex are configured and integrated. Few analyzers are enabled in the training VM:  

- _Abuse Finder_,
- _CyberCrime-Tracker_,
- _DShield\_lookup_,
- _File_Info_, _EMLParser_,
- _Fortiguard\_URLCategory_,
- _MaxMind GeoIP_,
- _UnshortenLink_,
- _TalosReputation_,
- _URLHaus, 
- _Urlscan\_io\_Search_ .

Report templates are preinstalled in all virtual machines.

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
