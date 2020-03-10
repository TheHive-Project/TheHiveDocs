# Migration to TheHive 4

## Supported version

The migration of TheHive from versions older than 3.4.0 is not possible. This is because the fact that the migration tool requires the database format that has been introduced by TheHive 3.4.0 and the migration to Elasticsearch 6 that came with some data structure changes (mostrly related to the definition of document relations)

So, if you want to test the migration, update your TheHive instance to TheHive 3.4.0+ before.

## How it works

The package TheHive4 comes with a migration tool (in /opt/thehive/bin/migrate) which can be used to import data from TheHive 3.4.0+.

In order to migrate the data, TheHive4 must be configured, in particular **database** and **file storage**. It also needs to connect to Elasticsearch instance used by your TheHive 3.4.0+

---

*⚠️* **Important Note**
In TheHive4, users are identified by their email addresses. In order to migrate users from TheHive3, a domain will be appended. The default domain is `thehive.local`, which must be changed *before* starting the migration. 

---

The default domain used to import existing users in, is configured in TheHive4 configuration file (`/etc/thehive/application.conf`), in `auth.defaultUserDomain` setting: 

```yaml
auth.defaultUserDomain: "mydomain.com"
```

In addition, update the authentication information as well. For instance, if a key is being used the authentication configuration block would be as follows:
```yaml
auth {
  providers: [
//    {name: session}               # required !
//    {name: basic, realm: thehive}
//    {name: local}
    {name: "bearer ***APIKEY***"}
  ]
# The format of logins must be valid email address format. If the provided login doesn't contain `@` the following
# domain is automatically appended
  defaultUserDomain: "example.com"
}
```

This domain will be appended to user accounts from TheHive 3.4.x.

Prior to running the `migrate` tool, connectivity can be tested by using
```bash
$curl http://ELASTICSEARCH_IP_ADDRESS:9200
{
  "name" : "R2-U361",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "***UUID***",
  "version" : {
    "number" : "5.6.16",
    "build_hash" : "3a740d1",
    "build_date" : "2019-03-13T15:33:36.565Z",
    "build_snapshot" : false,
    "lucene_version" : "6.6.1"
  },
  "tagline" : "You Know, for Search"
}
```

Once TheHive4 configuration file (`/etc/thehive/application.conf`) is correctly filled you can run migration tool:

```bash
/opt/thehive/bin/migrate \
  --output /etc/thehive/application.conf \
  --main-organisation myOrganisation \
  --es-uri http://ELASTICSEARCH_IP_ADDRESS:9200
```

The *Organisation* named *myOrganisation* is created by the migration tool and Users, Cases and Alerts from TheHive3 are created under that organisation.

More parameters are available, run `/opt/thehive/bin/migrate --help` for a summary.

---

⚠️ **Note**
The migration process can be very long, from several hours to several days, depending on the volume of data to migrate. TheHive4 can be started and used during migration. More recent data are migrated first.

---
