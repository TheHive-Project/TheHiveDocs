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

## Loadbalancer

In front of TheHive cluster, you can add a load-balancer which distributes http
requests to cluster nodes. One client doesn't need to use the same node
(affinity is not required).

Below an example (not optimized) of haproxy configuration :
```
# Global standard configuration, nothing specific for TheHive
global
        log /dev/log    local0
        log /dev/log    local1 notice
        chroot /var/lib/haproxy
        stats socket /run/haproxy/admin.sock mode 660 level admin
        stats timeout 30s
        user haproxy
        group haproxy
        daemon

        ca-base /etc/ssl/certs
        crt-base /etc/ssl/private

        ssl-default-bind-ciphers ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:RSA+AESGCM:RSA+AES:!aNULL:!MD5:!DSS
        ssl-default-bind-options no-sslv3

defaults
        log     global
        mode    http
        option  httplog
        option  dontlognull
        timeout connect 500
        timeout client  50000
        # server timeout must be at least the stream.refresh parameter in application.conf
        timeout server  2m
        errorfile 400 /etc/haproxy/errors/400.http
        errorfile 403 /etc/haproxy/errors/403.http
        errorfile 408 /etc/haproxy/errors/408.http
        errorfile 500 /etc/haproxy/errors/500.http
        errorfile 502 /etc/haproxy/errors/502.http
        errorfile 503 /etc/haproxy/errors/503.http
        errorfile 504 /etc/haproxy/errors/504.http


# Listen on all interfaces, on port 9000/tcp
frontend http-in
        bind *:9000
        default_backend servers

    # Configure all cluster node
    backend servers
        balance roundrobin
        server node1 10.0.0.1:9000 check
        server node2 10.0.0.2:9000 check
        server node3 10.0.0.3:9000 check
        server node4 10.0.0.4:9000 check
```

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
