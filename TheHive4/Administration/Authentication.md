# Authentication

**Note**: authentication is configured in the `conf/application.conf` file of TheHive.

Authentication consists of a set of module. Each one tries to authenticate the user. If it fails, the next one in the list is tried until the end of the list. The default configuration for authentication is:

```
auth {
  providers = [
    {name: session}
    {name: basic, realm: thehive}
    {name: local}
    {name: key}
  ]
}
```

Below are the available authentication modules:

## session

Authenticates HTTP requests using a cookie. This module manage the cookie creation and expiration. It accepts the configuration:

- inactivity (duration) the maximum time of user inactivity before the session is closed
- warning (duration) the time before the expiration TheHive returns a warning message

## local

Create a session if the provided login and password, or API key is correct according to the local user database.

## key

Authenticates HTTP requests using API key provided in the authorization header. The format is "Authorization: Bearer xxx" (xxx is replaced by the API key). The key is searched using other authentication modules (currently, only _local_ authentication module can validate the key).

## basic

Authenticates HTTP requests using the login and password provided in authorization header using basic authentication format (Base64). Password is checked from the local user database.

- realm (string) name of the realm. Without this parameter, the browser doesn't ask to authenticate.

## header

Authenticates HTTP requests using a HTTP header containing the user login. This is used to delegate authentication in a reverse proxy. This module accepts the configuration:

- userHeader (string) the name of the header that contain the user login

## ad

Use Microsoft ActiveDirectory to authenticate the user. The configuration is:

- winDomain (string) the Windows domain name (MYDOMAIN)
- dnsDomain (string) the Windows domain name in DNS format (mydomain.local)
- useSSL (boolean) indicate if SSL must be used to connect to domain controller. The global trust store of the JVM is used to validate remote certificate (JAVA_OPTS="-Djavax.net.ssl.trustStore=/path/to/truststore.jks")
- hosts (list of string) the addresses of the domain controllers. If missing, the dnsDomain is used.

## ldap

Use LDAP directory server to authenticate the user. The configuration is:

- bindDN (string) DN of the service account in LDAP. This account is used to search the user.
- bindPW (string) password of the service account.
- baseDN (string) DN where the users are located in.
- filter (string) filter used to search the user. "{0}" is replaced by the user login. A valid filter is: (&(uid={0})(objectClass=posixAccount))
- useSSL (boolean) indicate if SSL must be used to connect to LDAP server. The global trust store of the JVM is used to validate remote certificate (JAVA_OPTS="-Djavax.net.ssl.trustStore=/path/to/truststore.jks")
- hosts (list of string) the addresses of the LDAP servers.

## oauth2

Authenticate the user using an external OAuth2 authenticator server. The configuration is:

- clientId (string) client ID in the OAuth2 server.
- clientSecret (string) client secret in the OAuth2 server.
- redirectUri (string) the url of TheHive home page (.../index.html).
- responseType (string) type of the response. Currently only "code" is accepted.
- grantType (string) type of the grant. Currently only "authorization_code" is accepted.
- authorizationUrl (string) the url of the OAuth2 server.
- tokenUrl (string) the token url of the OAuth2 server.
- userUrl (string) the url to get user information in OAuth2 server.
- scope (list of string) list of scope
- userIdField (string) the field that contains the id of the user in user info
- userOrganisationField (string)
- defaultOrganisation (string)
- authorizationHeader (string)

## pki

This module is deprecated.

## Enable Multi-Factor Authentication

This feature requires a config property to be set to true:

```
auth.multifactor.enabled = true
```

Once enabled, users can configure their MFA through their User Settings page (top-Right corner button > Settings).

User administrators can:

- See which users have activated MFA
- Reset MFA settings of any user
