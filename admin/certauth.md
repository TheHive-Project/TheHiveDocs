# Single Sign-On with X.509 certificates
## Abstract
This guide tries to explain how to configure user authentication using client certificate. This feature is experimental and its workness is not guaranteed.

## Configure SSL

First TheHive must be configured as an SSL termination, without reverse proxy. This can be achieved by appending to configuration:
```
https.port: 9443
play.server.https.keyStore {
  path: "/path/to/keystore.jks"
  type: "JKS"
  password: "password_of_keystore"
}
```
You can find more details in [configuration guide](https://github.com/CERT-BDF/TheHiveDocs/blob/master/admin/configuration.md#10-https) and in [PlayFramework documentation](https://www.playframework.com/documentation/2.6.x/ConfiguringHttps).

## Configure certificate authority

A certificate must be provided to user. The certificate authority used to sign user certificate must be declared in TheHive. Once setup, all certificate issued by this authority will be trusted.

Certificate authority must be added to a trust store in the same manner than key store:
```
play.server.https.trustStore {
  path: "/path/to/trustStore.jks"
  type: "JKS"
  password: "password_of_truststore"
}
```

## Tell TheHive where it can find user name

The user name must be stored in user certificate. It can be in certificate subject (RDN) or in subject alternative names (SAN). Supported SAN fields are: upn, rfc822Name, dNSName, x400Address, directoryName, ediPartyName, uniformResourceIdentifier, iPAddress and registeredID (even if most of them have no sense for an user).

The setting `auth.pki.certificateField` must contain the name of the field which contains the user name.

```
auth.method.pki = true # enable PKI authentication method
auth.pki.certificateField = cn
```

**WARNING** make sure user exists in TheHive. PKI authentication doesn't prevent user creation.
