### Step 1: Install openSSL

### Step 2: Create an RSA Keypair:

 > openssl genrsa -des3 -passout pass:x -out xxx.key 2048
  
### Step 3: Extract the Private Key into the “httpd” Folder:

 > sudo mkdir /path/to/certificate/
  
 > openssl rsa -passin pass:x -in xxx.key -out /path/to/certificate/xx.xx.xx.xx.key
  
### Step 4: Creating a “Certificate Signing Request” (CSR) File:

 > openssl req -new -key /etc/httpd/httpscertificate/xx.xx.xx.xx.key -out /path/to/certificate//xx.xx.xx.xx.csr
  
### Step 5: Creating the Certificate “.crt” File:

 > openssl x509 -req -days 365 -in /path/to/certificate/xx.xx.xx.xx.csr -signkey /path/to/certificate/xx.xx.xx.xx.key -out /path/to/certificate/xx.xx.xx.xx.crt

### Step 6: Install Nginx

### Step 7: Edit "/etc/nginx/nginx.conf"

        # Settings for a TLS enabled server.
        
        server {
        
        (...)
        
        ssl_certificate "/path/to/certificate/xx.xx.xx.xx.crt";
        
        ssl_certificate_key "/path/to/certificate/xx.xx.xx.xx.key";
        
        ssl_session_cache shared:SSL:1m;
        
        ssl_session_timeout  10m;
        
        ssl_ciphers HIGH:!aNULL:!MD5;
        
        ssl_prefer_server_ciphers on;
        
        #        # Load configuration files for the default server block.
        
        include /etc/nginx/default.d/*.conf;
        
        location / {
        
          add_header              Strict-Transport-Security "max-age=31536000; includeSubDomains";
          
          proxy_pass              http://xx.xx.xx.xx:9000/;
          
          proxy_http_version      1.1;
          
        }
        

xx.xx.xx.xx = Machine IP address
