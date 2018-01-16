# TheHive cluster

TheHive is horizontally scalable. You can dynamically add node to your cluster
to increase the performance of the platform.
TheHive API is stateless, except for stream. For this reason, the cluster nodes
need to communicate with each other.
You can configure TheHive in a cluster from version 3.1.0.


The first node of the cluster has a specific role : it must initiate the cluster
creation. Then other nodes only needs to contact at least one node of the
cluster to join it. This is done by configuring "seed nodes".

The first node must have itself in the seed node. The other nodes must have at
least one already joined node in its seed node list.

**Note** : all cluster nodes must share the same secret (`play.http.secret.key` in
application.conf)

## Configuration

Define node1 (10.0.0.1) as first node of the cluster. Its configuration looks
like :
```
akka {
  remote {
    netty.tcp {
      hostname = "10.0.0.1"
      port = 2552
    }
  }
  # seed node is itself as it is the first node of the cluster
  cluster.seed-nodes = ["akka.tcp://application@10.0.0.1:2552"]
}
```

Then add another node (node2: 10.0.0.2) to our one-node cluster :
```
akka {
  remote {
    netty.tcp {
      hostname = "10.0.0.2"
      port = 2552
    }
  }
  # seed node list contains at least one active node
  cluster.seed-nodes = ["akka.tcp://application@10.0.0.1:2552"]
}
```

It is safer to define several seed nodes, except for first node. For example :

node  | configured seed nodes
------|----------------------
node1 | node1
node2 | node1, node3
node3 | node2, node4
node4 | node1, node2, node3

## Debug

You can enable debug messages with the following configuration :
```
akka {
  actor {
    debug {
      receive = on
      autoreceive = on
      lifecycle = on
      unhandled = on
    }
  }
}
```

## More details

TheHive uses akka cluster. You can refer to
[akka documentation](https://doc.akka.io/docs/akka/2.5/index-cluster.html) for
more details.
