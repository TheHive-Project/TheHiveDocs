You can find the default configuration settings of TheHive below:

```
# maximum number of similar cases
maxSimilarCases = 100

# ElasticSearch
search {
  # Name of the index
  index = the_hive
  # Name of the ElasticSearch cluster
  cluster = hive
  # Address of the ElasticSearch instance
  host = ["127.0.0.1:9300"]
  # Scroll keepalive
  keepalive = 1m
  # Size of the page for scroll
  pagesize = 50
  # Arbitrary settings
  settings {
    # Maximum number of nested fields
    mapping.nested_fields.limit = 50
  }
}

# Datastore
datastore {
  # Size of stored data chunks
  chunksize = 50k
  hash {
    # Main hash algorithm /!\ Don't change this value
    main = "SHA-256"
    # Additional hash algorithms (used in attachments)
    extra = ["SHA-1", "MD5"]
  }
  attachment.password = "malware"
}

auth {
	# "provider" parameter contains authentication provider. It can be multi-valued (useful for migration)
	# available auth types are:
	# local : passwords are stored in user entity (in ElasticSearch). No configuration are required.
	# ad : use ActiveDirectory to authenticate users. Configuration is under "auth.ad" key
	# ldap : use LDAP to authenticate users. Configuration is under "auth.ldap" key
	provider = [local]

	ad {
		# The name of the Microsoft Windows domaine using the DNS format. This parameter is required.
		#domainFQDN = "mydomain.local"

    # Optionally you can specify the host names of the domain controllers. If not set, TheHive uses "domainFQDN".
    #serverNames = [ad1.mydomain.local, ad2.mydomain.local]

		# The Microsoft Windows domain name using the short format. This parameter is required.
		#domainName = "MYDOMAIN"

		# Use SSL to connect to the domain controller(s).
		#useSSL = true
	}

	ldap {
		# LDAP server name or address. Port can be specified (host:port). This parameter is required.
		#serverName = "ldap.mydomain.local:389"

    # If you have multiple ldap servers, use the multi-valued settings.
    #serverNames = [ldap1.mydomain.local, ldap2.mydomain.local]

		# Use SSL to connect to directory server
		#useSSL = true

		# Account to use to bind on LDAP server. This parameter is required.
		#bindDN = "cn=thehive,ou=services,dc=mydomain,dc=local"

		# Password of the binding account. This parameter is required.
		#bindPW = "***secret*password***"

		# Base DN to search users. This parameter is required.
		#baseDN = "ou=users,dc=mydomain,dc=local"

		# Filter to search user {0} is replaced by user name. This parameter is required.
		#filter = "(cn={0})"
	}
}

# Maximum time between two requests without requesting authentication
session {
  warning = 5m
  inactivity = 1h
}

# Streaming
stream.longpolling {
  # Maximum time a stream request waits for new element
  refresh = 1m
  # Lifetime of the stream session without request
  cache = 15m
  nextItemMaxWait = 500ms
  globalMaxWait = 1s
}

# Cortex configuration
########

cortex {
  #"CORTEX-SERVER-ID" {
  #  # URL of MISP server
  #  url = ""
  #  #HTTP client configuration, more details in section 8
  #  ws {
  #    ws.useProxyProperties = true
  #    proxy {
  #      # The hostname of the proxy server.
  #      #host = ""
  #      # The port of the proxy server.
  #      #post = 0
  #      # The protocol of the proxy server.  Use "http" or "https".  Defaults to "http" if not specified.
  #      #protocol = "http"
  #      # The username of the credentials for the proxy server.
  #      #user = ""
  #      # The password for the credentials for the proxy server.
  #      #password = ""
  #      # The password for the credentials for the proxy server.
  #      #ntlmDomain = ""
  #      # The realm's charset.
  #      #encoding = ""
  #      # The list of host on which proxy must not be used.
  #      #nonProxyHosts = ""
  #    }
  #    ssl {
  #      keyManager { # used for client certificate authentication
  #        stores = [{
  #          type: "pkcs12" // JKS or PEM
  #          path: "mycert.p12"
  #          password: "password1"
  #        }]
  #      }
  #      # Add certificate authorities to trust remote certificate  
  #      trustManager {
  #        stores = [{
  #          type: "JKS" // JKS or PEM
  #          path: "keystore.jks"
  #          password: "password1"
  #        }]
  #     }
  #     debug = {
  #       ssl = false
  #       trustmanager = false
  #       keymanager = false
  #       sslctx = false
  #       handshake = false
  #       verbose = false
  #       data = false
  #       certpath = false
  #     }
  #
  #     # default SSL protocol
  #     #protocol = "TLSv1.2"
  #
  #     # list of enabled SSL protocols
  #     #ws.ssl.enabledProtocols = ["TLSv1.2", "TLSv1.1", "TLSv1"]
  #
  #     # SSL Cipher suite
  #     #enabledCipherSuites = [
  #     #  "TLS_DHE_RSA_WITH_AES_128_GCM_SHA256",
  #     #  "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
  #     #  "TLS_DHE_RSA_WITH_AES_256_GCM_SHA384",
  #     #  "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
  #     #]
  #    }
  #  }
  #}
}

# MISP configuration
########

misp {
  #"MISP-SERVER-ID" {
  #  # URL of MISP server
  #  url = ""
  #  # authentication key
  #  key = ""
  #  #tags to be added to imported artifact
  #  tags = ["misp"]
  #
  #  # filters:
  #  # the maximum number of attributes (max-attributes)
  #  #max-attributes = 1000
  #  # the maximum size of the event json message
  #  #max-size = 1 MiB
  #  # the age of the last publication
  #  #max-age = 7 days
  #  exclusion {
  #  # the organisation is black-listed  
  #  #organisation = ["bad organisation", "other orga"]
  #  # one of the tags is black-listed
  #  #tags = ["tag1", "tag2"]
  #  }
  #
  #  ws {
  #    ws.useProxyProperties = true
  #    proxy {
  #      # The hostname of the proxy server.
  #      #host = ""
  #      # The port of the proxy server.
  #      #post = 0
  #      # The protocol of the proxy server.  Use "http" or "https".  Defaults to "http" if not specified.
  #      #protocol = "http"
  #      # The username of the credentials for the proxy server.
  #      #user = ""
  #      # The password for the credentials for the proxy server.
  #      #password = ""
  #      # The password for the credentials for the proxy server.
  #      #ntlmDomain = ""
  #      # The realm's charset.
  #      #encoding = ""
  #      # The list of host on which proxy must not be used.
  #      #nonProxyHosts = ""
  #    }
  #
  #    ssl {
  #      keyManager { # used for client certificate authentication
  #        stores = [{
  #          type: "pkcs12" // JKS or PEM
  #          path: "mycert.p12"
  #          password: "password1"
  #        }]
  #      }
  #      # Add certificate authorities to trust remote certificate  
  #      trustManager {
  #        stores = [{
  #          type: "JKS" // JKS or PEM
  #          path: "keystore.jks"
  #          password: "password1"
  #        }]
  #     }
  #     debug = {
  #       ssl = false
  #       trustmanager = false
  #       keymanager = false
  #       sslctx = false
  #       handshake = false
  #       verbose = false
  #       data = false
  #       certpath = false
  #     }
  #
  #     # default SSL protocol
  #     #protocol = "TLSv1.2"
  #
  #     # list of enabled SSL protocols
  #     #ws.ssl.enabledProtocols = ["TLSv1.2", "TLSv1.1", "TLSv1"]
  #
  #     # SSL Cipher suite
  #     #enabledCipherSuites = [
  #     #  "TLS_DHE_RSA_WITH_AES_128_GCM_SHA256",
  #     #  "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
  #     #  "TLS_DHE_RSA_WITH_AES_256_GCM_SHA384",
  #     #  "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
  #     #]
  #    }
  #  }

  #}

  # Interval between two MISP event import
  interval = 1h

}

# Metrics configuration
########

metrics {
  name = default
  enabled = false
  rateUnit = SECONDS
  durationUnit = SECONDS
  jvm = true
  logback = true

  graphite {
    enabled = false
    host = "127.0.0.1"
    port = 2003
    prefix = thehive
    rateUnit = SECONDS
    durationUnit = MILLISECONDS
    period = 10s
  }

  ganglia {
    enabled = false
    host = "127.0.0.1"
    port = 8649
    mode = UNICAST
    ttl = 1
    version = 3.1
    prefix = thehive
    rateUnit = SECONDS
    durationUnit = MILLISECONDS
    tmax = 60
    dmax = 0
    period = 10s
  }

  influx {
    enabled = false
    url = "http://127.0.0.1:8086"
    user = root
    password = root
    database = thehive
    retention = default
    consistency = ALL
    #tags = {
    #	tag1 = value1
    #	tag2 = value2
    #}
    period = 10s
  }
}
```
