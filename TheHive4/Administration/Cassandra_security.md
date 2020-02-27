

**References**
- [https://docs.datastax.com/en/archived/cassandra/3.0/cassandra/configuration/secureInternalAuthenticationTOC.html](https://docs.datastax.com/en/archived/cassandra/3.0/cassandra/configuration/secureInternalAuthenticationTOC.html)

## Internal authentication

```sql
CREATE ROLE thehive WITH PASSWORD = 'thehive1234' AND LOGIN = true;
GRANT ALL PERMISSIONS ON KEYSPACE thehive TO thehive;
```

## SSL encryption

### Node to node encryption communication

### Client-to-node encrypted communication