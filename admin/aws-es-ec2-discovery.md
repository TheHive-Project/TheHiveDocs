### What this is
If you are planning to deploy your Hive instance to production on AWS and would like to add additional data/ingest/coordinator nodes to the current Hive cluster

### Preparation
* Set up an IAM role within the AWS IAM console and attach the EC2 discovery policy 
* Make note of new IAM user's role KeyID and AWS Secret
* Attach policy to every instance that's running ES (Master, and other nodes)

```
{
  "Statement": [
    {
      "Action": [
        "ec2:DescribeInstances"
      ],
      "Effect": "Allow",
      "Resource": [
        "*"
      ]
    }
  ],
  "Version": "2012-10-17"
}
```

Set `$JAVA_HOME` in `/etc/default/elasticsearch`:
```
sudo vi /etc/default/elasticsearch
JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/
```

Now set the JVM memory options to at least ½ of the memory on the machine.
ES says anything less than that will result in poor performance. (On 8 gb machine, 4 is half.)
```
sudo vim /etc/elasticsearch/jvm.options
-Xms4g
-Xmx4g
```

Set up EC2-discovery for AWS:
```
cd /usr/share/elasticsearch/bin
sudo ./elasticsearch-plugin install discovery-ec2
```

Set up Elasticsearch Keystore (for both Master + Node):
* Do this for every single one of the node/instance you are trying to connect to your Hive cluster
```
cd /usr/share/elasticsearch/bin
sudo ./elasticsearch-keystore create
sudo ./elasticsearch-keystore list
sudo ./elasticsearch-keystore add discovery.ec2.access_key (enter key when prompts)
sudo ./elasticsearch-keystore add discovery.ec2.secret_key (enter key when prompts)
sudo ./elasticsearch-keystore list
```

Once you’re done, it should look like this:
```
ubuntu@ip-x-x-x-x:/usr/share/elasticsearch/bin$ sudo ./elasticsearch-keystore list
discovery.ec2.access_key
discovery.ec2.secret_key
keystore.seed

```

### If you have ES running already:
Disable shard allocation
```
curl -H "Content-Type: application/json" -XPUT 'localhost:9200/_cluster/settings' -d '{ "persistent": { "cluster.routing.allocation.enable": "none" } }'
```

Stop ES:
```
sudo systemctl stop elasticsearch
```

Edit Elasticsearch settings:
```
sudo vi /etc/elasticsearch/elasticsearch.yml
```

Master Node Setting:
```
cluster.name: hive
node.name: hive-master

node.master: true
node.data: true
node.ingest: true

# path.data: /var/lib/elasticsearch
# path.logs: /var/log/elasticsearch

network.host: [_ec2_,_local_]

discovery.zen.hosts_provider: ec2
discovery.zen.ping.unicast.hosts: ["x.x.x.x", "x.x.x.x"]
discovery.zen.minimum_master_nodes: 1

discovery.ec2.any_group: true
discovery.ec2.host_type: private_ip

cloud.node.auto_attributes: true
cluster.routing.allocation.awareness.attributes: aws_availability_zone
discovery.ec2.tag.es_cluster: "hive-prod-elasticsearch"
discovery.ec2.endpoint: ec2.us-west-2.amazonaws.com

thread_pool.index.queue_size: 100000
thread_pool.search.queue_size: 100000
thread_pool.bulk.queue_size: 100000

```
* Replace `x.x.x.x` with your Elasticsearch instance's actual IP address
* Replace ec2 endpoint as appropriate

Data/Ingest/Master-eligible Node Setting:
Use the same config above.
Edit these as you see fit for your environment
```
node.name: hive-coordinator
node.master: true
node.data: true
node.ingest: true
```

Start ES back up:
```
sudo systemctl start elasticsearch
```

Check system health:
```
curl -XGET http://localhost:9200/_cluster/health?pretty=true
```

It should said there are 2 nodes running.

If anything is wrong, check the log:
```
sudo cat /var/log/elasticsearch/hive.log
```

Re-enable shard allocation:
```
curl -H "Content-Type: application/json" -XPUT 'localhost:9200/_cluster/settings' -d '{ "persistent": { "cluster.routing.allocation.enable": null } }'
```

