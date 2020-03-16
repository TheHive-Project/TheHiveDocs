

**Reference**: 

- https://docs.datastax.com/en/archived/cassandra/3.0/cassandra/operations/opsBackupRestore.html

## Cassandra

### Backup

- Before taking snapshots

```
nodetool cleanup thehive
```

- Take a snapshot
```
nodetool -h localhost -p 7199 snapshot thehive
```

- Remove old snapshots
```
nodetool -h localhost -p 7199 clearsnapshot -t <snapshotname>
```

- Restore snapshot 
The default folder structure under thehive keyspace looks as follows:
```
drwxr-xr-x  4 cassandra cassandra 4096 Mar 16 01:57 edgestore-UUID
drwxr-xr-x  4 cassandra cassandra 4096 Mar 16 01:57 edgestore_lock_-UUID
drwxr-xr-x  4 cassandra cassandra 4096 Mar 16 01:57 graphindex-UUID
drwxr-xr-x  4 cassandra cassandra 4096 Mar 16 01:57 graphindex_lock_-UUID
drwxr-xr-x  4 cassandra cassandra 4096 Mar 16 01:57 janusgraph_ids-UUID
drwxr-xr-x  4 cassandra cassandra 4096 Mar 16 01:57 system_properties-UUID
drwxr-xr-x  4 cassandra cassandra 4096 Mar 16 01:57 system_properties_lock_-UUID
drwxr-xr-x  4 cassandra cassandra 4096 Mar 16 01:57 systemlog-UUID
drwxr-xr-x  4 cassandra cassandra 4096 Mar 16 01:57 txlog-UUID
```

```
cp /var/lib/cassandra/data/thehive/<table_name-UUID>/snapshots/<snapshot_name> /var/lib/cassandra/data/thehive/<table_name-UUID>/  # Copy all snapshot files into the individual folders; copy the directory as-is into the table_name-UUID folder.  
nodetool -h localhost -p 7199 refresh -- thehive txlog
nodetool -h localhost -p 7199 refresh -- thehive systemlog
nodetool -h localhost -p 7199 refresh -- thehive system_properties
nodetool -h localhost -p 7199 refresh -- thehive edgestore
nodetool -h localhost -p 7199 refresh -- thehive graphindex
chown -R cassandra.root /var/lib/cassandra/ # Depending on where/how the backups are copied, chown helps fix any permissioning issues 
```


