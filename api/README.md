# TheHive API

TheHive exposes REST APIs through JSON over HTTP.

- [HTTP request format](request.md)
- [Authentication](authentication.md)
- [Model](model.md)
- [Alert](alert.md)
- [Case](case.md)
- [Observable](artifact.md)
- [Task](task.md)
- [Log](log.md)
- [User](user.md)
- [Connectors](connectors)

Caveats:
- Not all information is output using the API. In order to get information about more cases/alerts, please use *?range=a-b* in the URL, where a and b specify the range.
