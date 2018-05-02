# Schema version
The data of TheHive is stored in an ElasticSearch index. The name of the index
is suffixed by the revision of the schema. When the schema of TheHive database
changes, a new one is created and the version is incremented. By default, index
base name is "the_hive" but can be configured (`index.index` in
application.conf).

The following table show for each version of TheHive the default name of the
index:

| TheHive version | Index name  |
|-----------------|-------------|
| 2.9.1           | the_hive_7  |
| 2.9.2           | the_hive_7  |
| 2.10.0          | the_hive_8  |
| 2.10.1          | the_hive_8  |
| 2.10.2          | the_hive_8  |
| 2.11.0          | the_hive_9  |
| 2.11.1          | the_hive_9  |
| 2.11.2          | the_hive_9  |
| 2.11.3          | the_hive_9  |
| 2.12.0          | the_hive_10 |
| 2.12.1          | the_hive_10 |
| 2.13.0          | the_hive_10 |
| 2.13.1          | the_hive_10 |
| 2.13.2          | the_hive_11 |
| 3.0.0           | the_hive_12 |
| 3.0.1           | the_hive_12 |
| 3.0.2           | the_hive_12 |
| 3.0.3           | the_hive_12 |
| 3.0.4           | the_hive_13 |
