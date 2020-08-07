

**Reference**: 

- https://docs.datastax.com/en/archived/cassandra/3.0/cassandra/operations/opsBackupRestore.html

## Cassandra

### Backup

To backup or export database from Cassandra, following information are required: 

- Cassandra admin password

- keyspace used by thehive (default = `thehive`). This can be checked in the `application.conf`configuration file, in the database configuration in *storage*, *cql* and `keyspace` attribute. 

    ```
    [..]
    db.janusgraph {
      storage {
        backend: cql
        hostname: ["127.0.0.1"]
    
        cql {
          cluster-name: thp
          keyspace: thehive
        }
      }
    [..]
    ```

    

Considering that your keyspace is `thehive` and `backup_name` is the name of the snapshot, run the following commands:

- Before taking snapshots

```
nodetool cleanup cycling
```

- Take a snapshot
```
nodetool snapshot thehive -t backup_name
```

- Create and archive with the snapshot data: 

```
tar cjf backup.tbz /var/lib/cassandra/data/thehive/*/snapshots/backup_name/
```

- Remove old snapshots
```
nodetool -h localhost -p 7199 clearsnapshot -t <snapshotname>
```


