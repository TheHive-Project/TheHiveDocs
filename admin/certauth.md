# Single Sign-On on TheHive with X.509 Certificates
## Abstract

SSL managed by TheHive is known to have some stability problem. It is advise to not enable it in production and
configure SSL on a reverse proxy, in front of TheHive. This make X509 certificate authentication non applicable.

In order to do x509 authentication it is recommended to do it in the reverse proxy and then forward user identity to
TheHive in a HTTP header. This feature has been added in version 3.2.

**WARNING** This setup is valid only if nobody except the reverse proxy can connect to TheHive. Users must have to
use the reverse proxy. Otherwise, an user would be able to choose his identity on TheHive.
 
## Setup a reverse proxy

If you use nginx, the site configuration file should look like:
```
  server {
      listen 443 ssl;
      server_name thehive.example.com;
  
      ssl on;
      ssl_certificate         ssl/thehive_cert.pem;
      ssl_certificate_key     ssl/thehive_key.pem;
      
      # Force client to have a certificate
      ssl_verify_client       on;
  
      proxy_connect_timeout   600;
      proxy_send_timeout      600;
      proxy_read_timeout      600;
      send_timeout            600;
      client_max_body_size    2G;
      proxy_buffering off;
      client_header_buffer_size 8k;
  
      # Map certificate DN to user login stored in TheHive
      map $ssl_client_s_dn $thehive_user
      {
        default "";
        /C=FR/O=TheHive-Project/CN=Thomas toom;
        /C=FR/O=TheHive-Project/CN=Georges bofh;
      };

      # Redirect all request to local TheHive
      location / {
          add_header              Strict-Transport-Security "max-age=31536000; includeSubDomains";
          # Send the mapped user login to TheHive, in THEHIVE_USER HTTP header
          proxy_set_header        THEHIVE_USER $thehive_user;
          proxy_pass              http://127.0.0.1:9000/;
          proxy_http_version      1.1;
      }
  }
```

## Enable authentication delegation in TheHive

Setup TheHive to identify user by the configured HTTP header (THEHIVE_USER): 
```
auth {
  method.header = true
  header.name = THEHIVE_USER
}

# Listen only on localhost to prevent direct access to TheHive
http.address=127.0.0.1
```