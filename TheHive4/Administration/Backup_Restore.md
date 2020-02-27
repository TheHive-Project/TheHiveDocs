

**Reference**: 

- https://docs.datastax.com/en/archived/cassandra/3.0/cassandra/operations/opsBackupRestore.html

## Cassandra

### Backup

- Before taking snapshots

```
nodetool cleanup cycling
```

- Take a snapshot
```
nodetool -h localhost -p 7199 snapshot thehive
```

- Remove old snapshots
```
nodetool -h localhost -p 7199 clearsnapshot -t <snapshotname>
```


