# FAQ

## Table of Contents
  * [Installation and Administration](#installation-and-administration)
    * [Creation of the First Administrator Account](#creation-of-the-first-administrator-account)
    * [Where Does TheHive Store Its Logs?](#where-does-thehive-store-its-logs)
    * [Is there an Audit Trail?](#is-there-an-audit-trail)
  * [Templates](#templates)
    * [I Can't Add a Template](#i-cant-add-a-template)
    * [Why My Freshly Added Template Doesn't Show Up?](#why-my-freshly-added-template-doesnt-show-up)
  * [Analyzers](#analyzers)
    * [I Would Like to Contribute or Request a New Analyzer](#i-would-like-to-contribute-or-request-a-new-analyzer)
  * [MISP](#misp)
    * [Can I Use a Specific Template for Imported MISP Events?](#can-i-use-a-specific-template-for-imported-misp-events)
    * [Can I Import Events from Multiple MISP Servers?](#can-i-import-events-from-multiple-misp-servers)
  * [Miscellaneous Questions](#miscellaneous-questions)
    * [Can I Enable HTTPS to Connect to TheHive?](#can-i-enable-https-to-connect-to-thehive)
    * [Can I connect TheHive to an AWS ElasticSearch service?](#can-i-connect-thehive-to-an-aws-elasticsearch-service)
    * [Do you support Elasticsearch 5\.x?](#do-you-support-elasticsearch-5x)
    * [Do you support Elasticsearch 6\.x or later?](#do-you-support-elasticsearch-6x-or-later)


## Installation and Administration
### Creation of the First Administrator Account
After installing TheHive, the first connection to the Web UI triggers a database update. After that operation, you'll be prompted to create an administrator account. If this prompt is not completed, there is no way to set the admin password. Hence it will be impossible to connect to TheHive. To reset the operation, you need to delete the corresponding index from Elasticsearch. First, find out what is the current index of TheHive by running the following command on a host where the Elasticsearch DB used by TheHive is located:

```bash
$ curl http://127.0.0.1:9200/_cat/indices
```

The indexes that TheHive uses always start with`the_hive_` followed by a number. Let's assume that the output of the command is (**Warning**: this will delete everything)):

```bash
yellow open cortex_1    PC_pLFGBS5G2TNQYr4ajgw 5 1    611 6  2.1mb  2.1mb
yellow open the_hive_13 ft7GGTfhTr-4lSzZw5r1DQ 5 1 180160 4 51.5mb 51.5mb
```

In this example, the index used by TheHive is `the_hive_13`. To delete it, run the following command:

```bash
$ curl -X DELETE http://127.0.0.1:9200/the_hive_13
```

Then reload the page or restart TheHive.

### Where Does TheHive Store Its Logs?
Logs are stored in `/var/log/thehive/application.log`.

### Is there an Audit Trail?
Yes but you have to query directly the underlying Elasticsearch storage to get access to it:

```bash
curl -XPOST http://localhost:9200/the_hive_13/audit/_search
```

In the command above, we assume that TheHive's index is `the_hive_13`. To find out what is the current index of TheHive, run the following command on a host where the Elasticsearch DB used by TheHive is located:

```bash
$ curl http://127.0.0.1:9200/_cat/indices?
```

The indexes that TheHive uses always start with`the_hive_` followed by a number.

Alternatively, you may configure [Webhooks](admin/webhooks.md). When enabled, TheHive will send each action that has been performed on it (add case, update case, add task, ...), in real time, to an HTTP endpoint.

## Templates
### I Can't Add a Template
You need to log in as an administrator to add a template.

### Why My Freshly Added Template Doesn't Show Up?
When you add a new template and hit the `+NEW` button, you don't see it because unlike other events that you can see in the Flow, it is not broadcasted to all the user sessions. So you need to refresh the page before clicking the `+NEW` button.

You don't need to log out then log in again.


## Analyzers
### I Would Like to Contribute or Request a New Analyzer
If you'd like to develop or ask for an analyzer that will help you get the most out of TheHive, please open a [feature request](https://github.com/TheHive-Project/Cortex-Analyzers/issues/new) first. This will give us a chance to validate the use cases and avoid having multiple persons working on the same analyzer.

Once validated, you can either develop your analyzer or wait for TheHive Project or a contributor to undertake the task and if everything is alright, we will schedule its addition to a future Cortex release.

For a head start on analyzer development, please read the [corresponding page](https://github.com/TheHive-Project/CortexDocs/blob/master/api/how-to-create-an-analyzer.md) on the CortexDocs repository.

## MISP
### Can I Use a Specific Template for Imported MISP Events?
Definitely! You just need to add a `caseTemplate` parameter in the section corresponding to the MISP connector in your `conf/application.conf` file as  described in the [Administrator's Guide](/admin/configuration.md#7-misp) and create the case template in TheHive's Web UI. You need the `admin` role to do that.

### Can I Import Events from Multiple MISP Servers?
Yes, this is possible. For each MISP server, add a `misp` section in your `conf/application.conf` file as described in the [Administrator's Guide](admin/configuration.md#7-misp).

## Miscellaneous Questions

### Can I Enable HTTPS to Connect to TheHive?
Add the following lines to `/etc/thehive/application.conf`

    https.port: 9443
    play.server.https.keyStore {
      path: "/path/to/keystore.jks"
      type: "JKS"
      password: "password_of_keystore"
    }

HTTP can disabled by adding line `http.port=disabled`. Please read the [relevant section](admin/configuration.md#10-https) in the Configuration Guide.

* To import your certificate in the keystore, depending on your situation, you can follow [Digital Ocean's tutorial](https://www.digitalocean.com/community/tutorials/java-keytool-essentials-working-with-java-keystores).
* Make sure the keystore file is owned/can be accessed by the user running Cortex.

**Additional information**:
This is a setting of the Play framework that is documented on its website. Please refer to [https://www.playframework.com/documentation/2.5.x/ConfiguringHttps](https://www.playframework.com/documentation/2.5.x/ConfiguringHttps).

### Can I connect TheHive to an AWS ElasticSearch service?
AWS Elasticsearch service only supports HTTP transport protocol. It does not support the binary protocol which the Java client used by TheHive relies on to communicate with ElasticSearch. As a result, it is not possible to setup TheHive with AWS Elasticsearch service. More information is available at the following URLs:
- [http://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/aes-limits.html](https://www.elastic.co/guide/en/elasticsearch/reference/5.1/modules-network.html#_transport_and_http_protocols )

> “TCP Transport	: The service supports HTTP on port 80, but does not support TCP transport”

- [https://www.elastic.co/guide/en/elasticsearch/reference/5.1/modules-network.html#_transport_and_http_protocols](https://www.elastic.co/guide/en/elasticsearch/reference/5.1/modules-network.html#_transport_and_http_protocols)
> “TCP Transport : Used for communication between nodes in the cluster, by the Java Transport client and by the Tribe node.
> HTTP: Exposes the JSON-over-HTTP interface used by all clients other than the Java clients.”

### Do you support Elasticsearch 5.x?
Elasticsearch 5.x is supported starting from TheHive 2.13.0 (Mellifera 13). Please note that all versions starting from TheHive 2.13.0 support **only** ES 5 and **do not support ES2** anymore as it is very hard to support both. All versions preceding TheHive 2.13.0 supports only ES2.

### Do you support Elasticsearch 6.x or later?
No. Support for Elasticsearch 6.x or later is not currently planned as we are considering moving away from Elasticsearch in a future major release.