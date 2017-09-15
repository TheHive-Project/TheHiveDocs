# Authentication

Most API calls requires authentication. Credentials can be provided using a session cookie, an API key or directly using HTTP basic
authentication (if enabled).

Session cookie is suitable for browser authentication, not for a dedicated tool. The easiest solution if you want to
write a tool that use TheHive API is to use API key authentication. These key can be generated in user admin page in TheHive.
For example, to list cases, use the following curl
command:
```
# Using API key
curl -H 'Authorization: Bearer gvlvgck/user/api/key/dkS4Ywjz8Uf' http://127.0.0.1:9000/api/cases

# Using basic authentication
curl -u mylogin:mypassword http://127.0.0.1:9000/api/cases
```
