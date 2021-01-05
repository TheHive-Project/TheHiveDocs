# Authentication

**Note**: authentication is configured in the `conf/application.conf` file of TheHive.

Authentication consists of a set of module. Each one tries to authenticate the user. If it fails, the next one in the list is tried until the end of the list. The default configuration for authentication is:

```yaml
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
- redirectUri (string) the url of TheHive AOuth2 page (.../api/ssoLogin).
- responseType (string) type of the response. Currently only "code" is accepted.
- grantType (string) type of the grant. Currently only "authorization_code" is accepted.
- authorizationUrl (string) the url of the OAuth2 server.
- tokenUrl (string) the token url of the OAuth2 server.
- userUrl (string) the url to get user information in OAuth2 server.
- scope (list of string) list of scope
- userIdField (string) the field that contains the id of the user in user info
- organisationField (string, optional) the field that contains the organisation name in user info
- defaultOrganisation (string, optional) the default organisation used to login if not present on user info
- authorizationHeader (string) prefix of the authorization header to get user info: Bearer, token, ...

### User autocreation

To allow users to login without previously creating them, you can enable autocreation by adding `user.autoCreateOnSso=true` to the top level of your configuration.

### Example with **Keycloak**:

```yaml
auth {
  providers: [
    {name: session}               # required !
    {name: basic, realm: thehive}
    {name: local}
    {name: key}
    {
      name: oauth2
      clientId: "CLIENT_ID"
      clientSecret: "CLIENT_SECRET"
      redirectUri: "http://THEHIVE_URL/api/ssoLogin"
      responseType: "code"
      grantType: "authorization_code"
      authorizationUrl: "http://KEYCLOAK/auth/realms/TENANT/protocol/openid-connect/auth"
      authorizationHeader: "Bearer"
      tokenUrl: "http://KEYCLOAK/auth/realms/TENANT/protocol/openid-connect/token"
      userUrl: "http://KEYCLOAK/auth/realms/TENANT/protocol/openid-connect/userinfo"
      scope: ["openid", "email"]
      userIdField: "email"
    }
  ]
}
```

### Example with **Github**

```yaml
   {
      name: oauth2
      clientId: "CLIENT_ID"
      clientSecret: "CLIENT_SECRET"
      redirectUri: "http://THEHIVE_URL/api/ssoLogin"
      responseType: code
      grantType: "authorization_code"
      authorizationUrl: "https://github.com/login/oauth/authorize"
      authorizationHeader: "token"
      tokenUrl: "https://github.com/login/oauth/access_token"
      userUrl: "https://api.github.com/user"
      scope: ["user"]
      userIdField: "email"
      #userOrganisation: ""
    }
```

CLIENT_ID and CLIENT_SECRET are created in the _OAuth Apps_ section at [https://github.com/settings/developers](https://github.com/settings/developers).

**Note**: this configuration requires that users set the _Public email_ in their Public Profile on [https://github.com/settings/profile](https://github.com/settings/profile).

### Example with Microsoft 365

```yaml
    {
      name: oauth2
      clientId: "CLIENT_ID"
      clientSecret: "CLIENT_SECRET"
      redirectUri: "http://THEHIVE_URL/api/ssoLogin"
      responseType: code
      grantType: "authorization_code"
      authorizationUrl: "https://login.microsoftonline.com/TENANT/oauth2/v2.0/authorize"
      authorizationHeader: "Bearer "
      tokenUrl: "https://login.microsoftonline.com/TENANT/oauth2/v2.0/token"
      userUrl: "https://graph.microsoft.com/v1.0/me"
      scope: ["User.Read"]
      userIdField: "mail"
      #userOrganisation: "" ## if not existing in the response, use default organisation
    }
```

To create CLIENT_ID, CLIENT_SECRET and TENANT, register a new app at [https://aad.portal.azure.com/#blade/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/RegisteredApps](https://aad.portal.azure.com/#blade/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/RegisteredApps).

### Example with Google

```yaml
    {
      name: oauth2
      clientId: "CLIENT_ID"
      clientSecret: "CLIENT_SECRET"
      redirectUri: "http://THEHIVE_URL/api/ssoLogin"
      responseType: code
      grantType: "authorization_code"
      authorizationUrl: "https://accounts.google.com/o/oauth2/v2/auth"
      authorizationHeader: "Bearer "
      tokenUrl: "https://oauth2.googleapis.com/token"
      userUrl: "https://openidconnect.googleapis.com/v1/userinfo"
      scope: ["email", "profile", "openid"]
      userIdField: "email"
      # userOrganisation: "" ## if not existing in the response, use default organisation
    }
```

CLIENT_ID and CLIENT_SECRET are created in the _APIs & Services_ > _Credentials_ section of the [GCP Console](https://console.cloud.google.com/apis/credentials). Instructions on how to create Oauth2 credentials at [https://support.google.com/cloud/answer/6158849](https://support.google.com/cloud/answer/6158849). For the latest reference for Google auth URLs please check Google's [.well-known/openid-configuration](https://accounts.google.com/.well-known/openid-configuration).

## pki

This module is deprecated.

## Multi-Factor Authentication

Multi-Factor Authentication is enabled by default. This means users can configure their MFA through their User Settings page (top-Right corner button > Settings).

User administrators can:

- See which users have activated MFA
- Reset MFA settings of any user

This feature can be disabled by setting a config property tofalse:

```
auth.multifactor.enabled = false
```
