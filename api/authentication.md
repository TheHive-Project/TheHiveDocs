# Authentication

Most API calls require authentication. Credentials can be provided using a session cookie, an API key or directly using HTTP basic
authentication (when enabled).

Session cookie is suitable for browser authentication, not for a dedicated tool. The easiest solution if you want to
write a tool that leverages TheHive's API is to use API key authentication. API keys can be generated using the Web interface of the product, under the user admin area.
For example, to list cases, use the following curl
command:
```
# Using API key
curl -H 'Authorization: Bearer ***API*KEY***' http://127.0.0.1:9000/api/case
```

TheHive also supports basic authentication (disabled by default). You can enable it by adding `auth.method.basic=true` in the configuration file.
```
# Using basic authentication
curl -u mylogin:mypassword http://127.0.0.1:9000/api/case
```
