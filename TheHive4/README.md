# TheHive 4 : Installation, administration and user guides

![](files/thehive-logo.png)

[![Join the chat at https://gitter.im/TheHive-Project/TheHive](https://badges.gitter.im/TheHive-Project/TheHive.svg)](https://gitter.im/TheHive-Project/TheHive?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

This is the dedicated documentation for TheHive 4. The current version released is TheHive 4.0-RC1. 



---

⚠️ This version - like all RCx versions - is **not recommended** for production use ⚠️

---



Starting from TheHive 4.0-RC1, the application stack has completely been reviewed. TheHive do not rely on Elasticsearch anymore to store its data and the backend has been rewritten to support graph database schema.

TheHive is now supporting different data and files storage methods. However, even for a standalone server and for production uses:

- We strongly recommend using Apache Cassandra as a scalable and fault-tolerant database;

- For files, local filesystem is a good and simple choice.

For cluster configuration, we strongly recommends using Apache Hadoop as a distributed filesystem to store files.


## Notes

- The documentation is illustrated using Ubuntu 18.04 LTS as base system. 

## Hardware Pre-requisites

TheHive uses ElasticSearch to store data. Both software use a Java VM. We recommend using a virtual machine with 8vCPU, 8GB of RAM and 60 GB of disk. You can also use a physical machine with similar specifications.

## Installation and configuration Guides

This section is a step-by-step [installation and configuration guide](Installation/README.md) aiming at getting an instance of TheHive 4 up and running. This guide contains everything to:

- [Prepare your environment](Installation/README.md#java_virtual_machine) by installing and configuring dependencies and database softwares
- [Get and install TheHive binaries](Installation/Packages_and_binaries.md)


## Administration Guides

[Administration guides](Administration/README.md) can help you leverage or enable more advanced features, or setup a more complex architecture. 

## User guides

### Quick start

After installation, follow the [quick start guide](User/Quick-start.md) to access TheHive 4 with administrative permissions and create your first organisation. 

### Use TheHive as Administrator

- [Manage Organisations & Users](User/manage_orgs_users.md)
	- Introducing Roles and Shares
	- Create/Update/Delete Organisations
	- Create/Update/Delete Users
	- Link Organisations
- [Add report templates](User/Report_templates.md)
- [CustomFields](User/CustomFields.md)

### < TBC > 




## REST API


## License
TheHive is an open source and free software released under the [AGPL](https://github.com/TheHive-Project/TheHive/blob/master/LICENSE) (Affero General Public License). We, TheHive Project, are committed to ensure that TheHive will remain a free and open source project on the long-run.

## Updates
Information, news and updates are regularly posted on [TheHive Project Twitter account](https://twitter.com/thehive_project) and on [the blog](https://blog.thehive-project.org/).

## Contributing
We welcome your contributions. Please feel free to fork the code, play with it, make some patches and send us pull requests using [issues](https://github.com/TheHive-Project/TheHive/issues).

We do have a [Code of conduct](code_of_conduct.md). Make sure to check it out before contributing.

## Support
Please [open an issue on GitHub](https://github.com/TheHive-Project/TheHive/issues) if you'd like to report a bug or request a feature. We are also available on [Gitter](https://gitter.im/TheHive-Project/TheHive) to help you out.

If you need to contact the Project's team, send an email to <support@thehive-project.org>.

**Important Note**:

- If you have problems with [TheHive4py](https://github.com/TheHive-Project/TheHive4py), please [open an issue on its dedicated repository](https://github.com/TheHive-Project/TheHive4py/issues/new).
- If you encounter an issue with Cortex or would like to request a Cortex-related feature, please [open an issue on its dedicated GitHub repository](https://github.com/TheHive-Project/Cortex/issues/new).
- If you have troubles with a Cortex analyzer or would like to request a new one or an improvement to an existing analyzer, please open an issue on the [analyzers' dedicated GitHub repository](https://github.com/TheHive-Project/cortex-analyzers/issues/new).

## Community Discussions
We have set up a Google forum at <https://groups.google.com/a/thehive-project.org/d/forum/users>. To request access, you need a Google account. You may create one [using a Gmail address](https://accounts.google.com/SignUp?hl=en) or [without it](https://accounts.google.com/SignUpWithoutGmail?hl=en).

## Website
<https://thehive-project.org/>

