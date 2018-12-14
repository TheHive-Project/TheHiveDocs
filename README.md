![](images/thehive-logo.png)


[![Join the chat at https://gitter.im/TheHive-Project/TheHive](https://badges.gitter.im/TheHive-Project/TheHive.svg)](https://gitter.im/TheHive-Project/TheHive?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

TheHive is a scalable 4-in-1 open source and free security incident response platform designed to make life easier for SOCs, CSIRTs, CERTs and any information security practitioner dealing with security incidents that need to be investigated and acted upon swiftly. Thanks to [Cortex](https://github.com/TheHive-Project/Cortex/), our powerful free and open source analysis engine, you can analyze (and triage) observables at scale using more than 100 analyzers.

Additionally and starting from TheHive 3.1.0, you can actively respond to threats and interact with your constituency and other parties thanks to Cortex responders.

Last but not least, TheHive is highly integrated with [MISP](http://misp-project.org/), the *de facto* standard of threat sharing, as it can pull events from several MISP instances and export investigation cases back to one or several ones. It also has additional features such as MISP extended events and health checking.

**Note:**  This is TheHive's documentation repository. If you are looking for its source code, please visit [https://github.com/TheHive-Project/TheHive/](https://github.com/TheHive-Project/TheHive/).

## Hardware Pre-requisites

TheHive uses ElasticSearch to store data. Both software use a Java VM. We recommend using a virtual machine with 8vCPU, 8
GB of RAM and 60 GB of disk. You can also use a physical machine with similar specifications.


## Guides
- [Installation Guide](installation/install-guide.md)
- [Administration Guide](admin/admin-guide.md)
- [Configuration Guide](admin/configuration.md)
- [Webhooks](admin/webhooks.md)
- [Cluster Configuration](admin/cluster.md)
- [Updating](admin/updating.md)
- [Backup & Restore](admin/backup-restore.md)
- [Migration Guide](migration-guide.md)
- [API Documentation](api/README.md) (incomplete)
- [Cluster Configuration](admin/cluster.md)

## Miscellaneous Information
- [Feature Set](feature-set.md) **(Under Progress)**
- [Changelog](https://github.com/TheHive-Project/TheHive/blob/master/CHANGELOG.md)
- [FAQ](FAQ.md)
- [Presentations](presentations/list.md)
- [Training Material](training-material.md)
- [Single Sign-On on TheHive with X.509 Certificates](admin/certauth.md) **(Experimental Feature)**

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
