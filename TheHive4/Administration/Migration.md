Migration from version of TheHive older than 3.4.0 is not possible.

If you want to test the migration, update your TheHive instance to TheHive 3.4.0+ before.

The package TheHive4 comes with a migration tool (in /opt/thehive/bin/migrate)
which can be used to import data from TheHive 3.4.0+.
In order to migration the data, TheHive4 must be configured, in particular
database and file storage. It also needs to connect to Elasticsearch instance.

*⚠️* **Note:**
In TheHive4 users are identified by his email address. In order to migrate users
from TheHive3, a domain will be appended. The default domain is `thehive.local`,
which should be changed *before* starting the migration. This domain is
configure in TheHive4 configuration file, in `auth.defaultUserDomain` setting.

Once TheHive4 configuration file (`/etc/thehive/application.conf`) is correctly
filled you can run migration tool:

```
/opt/thehive/bin/migration \
  --output /etc/thehive/application.conf \
  --main-organisation myOrganisation \
  --es-uri http://127.0.0.1:9200
```

Users, cases and alerts from TheHive3 will be created under the organisation
specified by `--main-organisation` parameter.

More parameters are available, run `/opt/thehive/bin/migration --help`
for a summary.

*⚠️* **Note:**
The migration process can be very long, from several hours to several days,
depending on the volume of data to migrate. TheHive4 can be started and used
during migration. More recent data are migrated first.
