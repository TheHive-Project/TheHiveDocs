## Training Material
TheHive Project maintains a training virtual machine (OVA) containing TheHive, Cortex and Cortex analyzers with all dependencies and ElasticSearch installed on top of Ubuntu 16.04 with Oracle JRE 8.

As of this writing, the training VM includes Cerana 0.10 (TheHive 3.0.10), Cortex 2.0.4, TheHive4py 1.4.3, Cortex4py 1.0.0 and any available Cortex analyzer as of June 2, 2018.

**Warning**: The training VM is solely intended to be used for testing or training purposes. **We strongly encourage you to refrain from using it in production**.


### TL;DR

- Training VM system account : `thehive/thehive1234`
- TheHive URL : http://IP_OF_VM:9000
- Cortex URL : http://IP_OF_VM:9001
- Cortex superAdmin account : `admin/thehive1234`
- Cortex "training" Org admin account  : `thehive/thehive1234` (its key API is used to enable Cortex service in TheHive)

### Get It

You can download the VM from the following location:

[https://drive.google.com/open?id=0B3G-Due88gfQMzlfZ2t6RVhqTUk](https://drive.google.com/open?id=0B3G-Due88gfQMzlfZ2t6RVhqTUk)

To ensure that your download went through nicely, **check the file’s SHA256 hash** which must be equal to the following value:

`b5be8c927f37a975a8050d57e907a5b49a090d0dbe21b4b17766d5e10756a673`

**Note**: On starting the newly imported VM from OVA file in VMware Fusion, you may encounter a message asking to upgrade the virtual machine. By clicking on the `Upgrade` button you would be able to use the VM as expected.

![](images/training-vm-vmware-fusion-ova-upgrade_msg.png)

#### Previous Version

The previous version of the training VM, with Cerana 0.9 (TheHive 3.0.9), Cortex 2.0.4, TheHive4py 1.4.3, Cortex4py 1.0.0 and all Cortex analyzers as of Apr 28, 2018 is still available at the following address:

[https://drive.google.com/open?id=0B3G-Due88gfQMzZoWGdhYUJzZ28](https://drive.google.com/open?id=0B3G-Due88gfQMzdydXFuYXR4bFU)

To ensure that your download went through nicely, **check the file’s SHA256 hash** which must be equal to the following value:

`4c1c4d29f5a077cae117555f6e746c83127439d0d07e0061c3547c4430d37397`


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

- [download the report template package](https://dl.bintray.com/thehive-project/thehive/report-templates.zip)
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
