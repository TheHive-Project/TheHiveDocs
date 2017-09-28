## Training Material
TheHive Project maintains a training virtual machine (OVA) containing TheHive, Cortex and Cortex analyzers with all dependencies and ElasticSearch installed on top of Ubuntu 16.04 with Oracle JRE 8.

As of this writing, the training VM includes Mellifera 13.1 (TheHive 2.13.1 ), Cortex 1.1.4, TheHive4py 1.3.1, Cortex4py 1.0.0 and the latest Cortex analyzers as of Sep 25, 2017.

**Warning**: The training VM is solely intended to be used for testing or training purposes. **We strongly encourage you to refrain from using it in production**.

### Get It

You can download the VM from the following location:

[https://drive.google.com/file/d/0B3G-Due88gfQamJfZmZtYTFZVmM/view?usp=sharing](https://drive.google.com/file/d/0B3G-Due88gfQamJfZmZtYTFZVmM/view?usp=sharing)

To ensure that your download went through nicely, **check the file’s SHA256 hash** which must be equal to the following value:


`6745b923c2e13e91641453ed247fd8d1d0fdb47fc4150bd846538a0e46e4e5a1`

The system’s login is `thehive` and the associated password is `thehive1234`.

### Use It

You can start using TheHive & Cortex once the VM is started. To access TheHive, point your browser to the following URL:

[http://IP_OF_VM:9000](http://IP_OF_VM:9000)

For Cortex, the port is 9999:

[http://IP_OF_VM:9999](http://IP_OF_VM:9999)

### Configure TheHive

The first time you access TheHive, you’ll need to create the associated database by clicking on the `Update Database` button as shown below:

![](images/thehive-first-access_screenshot.png)

TheHive’s configuration file is located in `/etc/thehive/application.conf`. For additional configuration, [read the documentation](https://github.com/CERT-BDF/TheHiveDocs).

#### Cortex

TheHive is already configured to use the local Cortex service.

#### Analyzer and Associated Report Templates

To fully benefit from the analyzers, you should install the associated report templates:

- [download the report template package](https://dl.bintray.com/cert-bdf/thehive/report-templates.zip)
- log in TheHive using an administrator account
- go to Admin > Report templates menu
- click on Import templates button and select the downloaded package


#### Plug it with MISP

The test VM does not contain a MISP instance and none is configured in TheHive’s configuration file.  To play with MISP, you may want to [use the VM our good friends at CIRCL provide](https://www.circl.lu/services/misp-training-materials/).  Once you’ve downloaded it or if you have an existing instance, edit `/etc/thehive/application.conf` and [follow the configuration guide](https://github.com/CERT-BDF/TheHiveDocs/blob/master/admin/configuration.md#7-misp).

#### Restart or Go Mad

After each modification of `/etc/thehive/application.conf` do not forget to restart the service:

`$ sudo service thehive restart`

#### Troubles?

TheHive service logs are located in `/var/log/thehive/application.log`.

### Configure Cortex

All available analyzers are installed with their dependencies, but none is configured. To configure analyzers, edit `/etc/cortex/application.conf` and follow the configuration guide.

#### Restart or Go Mad

After each modification of `/etc/cortex/application.conf` do not forget to restart the service:

`$ sudo service cortex restart`

#### Troubles?

Cortex service logs are located in `/var/log/cortex/application.log`.

#### Need Help?

Something does not work as expected? No worries, we got you covered. Please join our  [user forum](https://groups.google.com/a/thehive-project.org/forum/#!forum/users), contact us on [Gitter](https://gitter.im/TheHive-Project/TheHive), or send us an email at [support@thehive-project.org](mailto:support@thehive-project.org). We are here to help.