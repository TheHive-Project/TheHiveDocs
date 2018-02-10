# Single Sign-On on TheHive with X.509 Certificates
## Abstract
This guide tries to explain how to configure user authentication on TheHive using X.509 client certificates. **This feature is experimental**. There is no guarantee that it will work.

## Step 0: Create the Users in TheHive
SSO is used for authentication for users which have existing accounts in TheHive. Make sure the users exist in TheHive. PKI authentication doesn't replace user creation.

## Step 1: Configure SSL
The first step consists of configuring SSL on TheHive, without resorting to a reverse proxy such as Nginx for such an endeavor. This can be achieved by appending the following lines to TheHive's configuration file (`/etc/thehive/application.conf`):
```
https.port: 9443
play.server.https.keyStore {
  path: "/path/to/keystore.jks"
  type: "JKS"
  password: "password_of_keystore"
}
```
You can find more details in the [configuration guide](configuration.md#10-https) and in the [PlayFramework documentation](https://www.playframework.com/documentation/2.6.x/ConfiguringHttps).

## Step 2: Configure a Certificate Authority
A certificate must be provided to each user who is going to single-sign on. The certificate authority which is used to to sign the user certificated must be declared in TheHive. Once setup, all certificates issued by this authority will be trusted.

A certificate authority must be added to a trust store in the same manner as a key store:
```
play.server.https.trustStore {
  path: "/path/to/trustStore.jks"
  type: "JKS"
  password: "password_of_truststore"
}
```

## Step 3: Tell TheHive where it Can Find the User Name
The user name must be stored in the user certificate. It can be in the certificate subject (RDN) or in the subject alternative names (SAN). Supported SAN fields are: upn, rfc822Name, dNSName, x400Address, directoryName, ediPartyName, uniformResourceIdentifier, iPAddress and registeredID (even if most of them have no sense for a user).

The setting `auth.pki.certificateField` must contain the name of the field which holds the user name. In the example below, we assume that it is in the CN:

```
auth.method.pki = true # enable PKI authentication method
auth.pki.certificateField = cn
```
