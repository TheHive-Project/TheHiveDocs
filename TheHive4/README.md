<div>
  <p align="center">
    <img src="Files/thehive-logo.png"width="600"/>  
  </p>
</div>
<div>
  <p align="center">
    <a href="https://chat.thehive-project.org" target"_blank"><img src="https://img.shields.io/badge/chat-on%20discord-7289da.svg?sanitize=true" alt="Discord"></a>
    <a href><img src="https://drone.strangebee.com/api/badges/TheHive-Project/TheHive/status.svg?ref=refs/heads/master" alt="Build status"></a>
    <a href="./LICENSE" target"_blank"><img src="https://img.shields.io/github/license/TheHive-Project/TheHive" alt="License"></a>        
  </p>
</div>

# TheHive 4 : Installation, administration and user guides

This documentation is dedicated to the all new TheHive 4. As of this writing, the latest release is TheHive 4.0.0-1. 

The application stack of TheHive 4 has been completely changed. TheHive 4 does not rely on Elasticsearch anymore to
 store its data and the backend has been rewritten to support graph databases.

TheHive now supports different data and files storage methods. However, even for a standalone, production server, we
 strongly recommend using Apache Cassandra as a scalable and fault-tolerant database. Files (attached to cases) can
  be stored on the local filesystem.

For cluster configurations, we strongly recommend using Apache Hadoop as a distributed filesystem to store files.

## Hardware Pre-requisites

Hardware requirements depends on the number of concurrent users and how they use the system. The following table give some information to choose the hardware.

| Number of users | CPU  | RAM   |
| --------------- | ---- | ----- |
| < 3             | 2    | 4-8   |
| < 10            | 4    | 8-16  |
| < 20            | 8    | 16-32 |

## Guides

- [Installation and configuration guides](Installation/README.md) : contain step-by-step installation instructions for
 TheHive 4 for different operating systems as well as corresponding binary archives.
- [Migration guide](Administration/Migration.md): how to migrate your data from TheHive 3.4.0+.
- [Administration guides](Administration/README.md): can help you leverage or enable more advanced features, or setup
 a more complex architecture.
- [User guides](User/README.md): including a [Quick start guide](User/Quick-start.md) to get your instance of TheHive
 ready to use.

## Webhooks
Webhooks were not integrated in TheHive 4.0-RC1, but are available since TheHive-4.0-RC2. They are now part of a new notification system that is almost ready but which still needs some work. The basic webhook functionality of the TheHive-3.x releases can be configured as described [here](Administration/Webhook.md). 

## License
TheHive is an open source and free software released under the [AGPL](https://github.com/TheHive-Project/TheHive/blob/master/LICENSE) (Affero General Public License). We, TheHive Project, are committed to ensure that TheHive will remain a free and open source project on the long-run.

## Updates
Information, news and updates are regularly posted on [TheHive Project Twitter account](https://twitter.com/thehive_project) and on [the blog](https://blog.thehive-project.org/).

## Contributing
We welcome your contributions. Please feel free to fork the code, play with it, make some patches and send us pull requests using [issues](https://github.com/TheHive-Project/TheHive/issues).

We do have a [Code of conduct](../code_of_conduct.md). Make sure to check it out before contributing.

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

