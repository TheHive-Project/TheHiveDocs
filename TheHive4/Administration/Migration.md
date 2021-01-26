# Migration to TheHive 4

TheHive 4.0 is delivered with a tool to migrate your data from TheHive 3.x. stored in Elasticsearch. 

## Supported versions

The tool only supports migration **from TheHive 3.4.0** and higher. 

Technically, many reasons explain this limitation: 

- A new database format has been introduced with TheHive 3.4.0,
- Elasticsearch 6.x came with changes in data structure (mostly related to the definition of document relations)  

So, if you want to migrate your data from TheHive 3 to TheHive 4.0, you are invited to update your current instance to TheHive 3.4.0+ before.

## How it works

All packages of TheHive4 distributed come with the migration program which can be used to import data from TheHive 3.4.0+. By default, it is installed in `/opt/thehive/bin/migrate`. 

### Pre-requisite

In order to migrate the data: 

- TheHive 4 **must** be installed on the system running the migration tool; 

- TheHive4 **must** be configured ; in particular **database** and **file storage** ;  
- The service `thehive` **must be stopped** (`service thehive stop`) . 

This tools **must** also have access to Elasticsearch database (http://ES:9200) used by TheHive 3, and the configuration file of TheHive 3.x instance. 

### Configuration of TheHive 4

---
⚠️ **Important Note**

In TheHive4, users are identified by their email addresses. Thus, a domain will be appended to usernames in order to migrate users from TheHive 3. 
TheHive 4.0 comes with a default domain named `thehive.local`. Starting the migration without explicitely specifying a domain name will result in migrating all users with a username formatted like  `user@thehive.local`. 

---

Change the default domain name used to import existing users in the configuration file of TheHive4 (`/etc/thehive/application.conf`) ;  add or update the setting named  `auth.defaultUserDomain`: 

```yaml
auth.defaultUserDomain: "mydomain.com"
```

This way, the domain `mydomain.com` will be appended to user accounts imported from TheHive 3.4+ (`user@mydomain.com`).

### Run the migration

Once TheHive4 configuration file (`/etc/thehive/application.conf`) is correctly filled you can run migration tool.

The program comes with a large set of options: 

```
# /opt/thehive/bin/migrate --help
TheHive migration tool 4.0.4-1
Usage: migrate [options]

  -v, --version
  -h, --help
  -c, --config <file>      global configuration file
  -i, --input <file>       TheHive3 configuration file
  -o, --output <file>      TheHive4 configuration file
  -d, --drop-database      Drop TheHive4 database before migration
  -m, --main-organisation <organisation>
  -u, --es-uri http://ip1:port,ip2:port
                           TheHive3 ElasticSearch URI
  -i, --es-index <index>   TheHive3 ElasticSearch index name
  -a, --es-keepalive <duration>
                           TheHive3 ElasticSearch keepalive
  -p, --es-pagesize <value>
                           TheHive3 ElasticSearch page size
  --max-case-age <duration>
                           migrate only cases whose age is less than <duration>
  --min-case-age <duration>
                           migrate only cases whose age is greater than <duration>
  --case-from-date <date>  migrate only cases created from <date>
  --case-until-date <date>
                           migrate only cases created until <date>
  --case-from-number <number>
                           migrate only cases from this case number
  --case-until-number <number>
                           migrate only cases until this case number
  --max-alert-age <duration>
                           migrate only alerts whose age is less than <duration>
  --min-alert-age <duration>
                           migrate only alerts whose age is greater than <duration>
  --alert-from-date <date>
                           migrate only alerts created from <date>
  --alert-until-date <date>
                           migrate only alerts created until <date>
  --include-alert-types <type>,<type>...
                           migrate only alerts with this types
  --exclude-alert-types <type>,<type>...
                           don't migrate alerts with this types
  --include-alert-sources <source>,<source>...
                           migrate only alerts with this sources
  --exclude-alert-sources <source>,<source>...
                           don't migrate alerts with this sources
  --max-audit-age <duration>
                           migrate only audits whose age is less than <duration>
  --min-audit-age <duration>
                           migrate only audits whose age is greater than <duration>
  --audit-from-date <date>
                           migrate only audits created from <date>
  --audit-until-date <date>
                           migrate only audits created until <date>
  --include-audit-actions <value>
                           migration only audits with this action (Update, Creation, Delete)
  --exclude-audit-actions <value>
                           don't migration audits with this action (Update, Creation, Delete)
  --include-audit-objectTypes <value>
                           migration only audits with this objectType (case, case_artifact, case_task, ...)
  --exclude-audit-objectTypes <value>
                           don't migration audits with this objectType (case, case_artifact, case_task, ...)
Accepted date formats are "yyyyMMdd[HH[mm[ss]]]" and "MMdd"
The Format for duration is: <length> <unit>.
Accepted units are:
  DAY:         d, day
  HOUR:        h, hr, hour
  MINUTE:      m, min, minute
  SECOND:      s, sec, second
  MILLISECOND: ms, milli, millisecond
```

Most of these options are filters you can apply to the program. For example, you could decide to import only some of the Cases/Alerts from your old instance: 

- Import Cases/Alerts not older than X days/hours,
- Import Cases/Alerts with the ID number,
- Import part of Audit trail
- ...

Taking the assumption that you are migrating a database hosted in a remote server, with TheHive 3, a basic command line to migrate data to a new instance will be like: 

```bash
/opt/thehive/bin/migrate \
  --output /etc/thehive/application.conf \
  --main-organisation myOrganisation \
  --es-uri http://ELASTICSEARCH_IP_ADDRESS:9200 \
  --es-index the_hive
```

with: 

- `--output` specifying the configuration file of TheHive 4.0 (the one that has previously been configured with at least, the **database** and **file storage**);
- `--main-organisation` specifying the *Organisation* named *myOrganisation* to create during the migration. The tool will then create Users, Cases and Alerts from TheHive3 under that organisation;
- `--es-uri`specifies the URL of the Elasticsearch server. If using authentication on Elasticsearch, `--input` option with a configuration file for TheHive3 is required;
- `--es-index` specified the index used in Elasticsearch. 



---

⚠️ **Note**

The migration process can be very long, from several hours to several days, depending on the volume of data to migrate. We **highly** recommand to not start the application during the migration.

---


### Using authentication on Cassandra

if you are using a dedicated account on Cassandra to access TheHive 4 data, this user must have permissions to create keyspaces on the database: 

```cql
GRANT CREATE on ALL KEYSPACES to username;
```


### Migration logs

#### Progress

The migration tool generates some logs during the process. By default, every 10 sec. a log is generated with information regarding the situation of the migration: 

```
[info] o.t.t.m.Migrate - [Migrate cases and alerts] CaseTemplate/Task:32 Organisation:1/1 Case/Task:160/201 Case:31/52 Job:103/138 ObservableType:3/17 Alert:25/235 Audit:3207/2986 CaseTemplate:6/6 Alert/Observable:700(52ms) Case/Observable:1325/1665 User:9/9 CustomField:13/13 Case/Task/Log:20/27
```

---
⚠️ **Note**

Numbers of Observables, Cases and others are estimations and not a definite value as computing these number can be very tedious. 

---


#### Warning regarding some files

It is important to notice that migrating Cases/Alerts containing MISP event that were imported with TheHive 2.13 (_Sept 2017_) or older, will cause observable files not being imported in TheHive 4. Indeed, until this version, TheHive referenced the file to the `AttributeId` in MISP and was not automatically downloaded. It then could generate a log like this: 

```
[warn] o.t.t.m.t.Input - Pre 2.13 file observables are ignored in MISP alert ffa3a8503ab0cd4f99fc6937a8e9b827
```


### Starting TheHive 4

Once the migration process is sucessfully completed, TheHive4 can be started. 

---
⚠️ **Important Note**

During the first start data are indexed and service is not available ; this can take some time. Do not stop or restart the service at this time. 
 
---


