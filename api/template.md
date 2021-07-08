# Template

## Model definition

Required attributes:
<TODO>
Optional attributes:
<TODO>

## Template manipulation

### Template methods


|HTTP Method |URI                                     |Action                                |
|------------|----------------------------------------|--------------------------------------|
|POST        |/api/case/template/_search              |Find a template                       |
|POST        |/api/case/template                      |Create a template                     |
|GET         |/api/case/template/:templateId          |Get a template                        |
|PATCH       |/api/case/template/:templateId          |Update a template                     |

### Create a template

#### Example
```
curl  -H 'Authorization: Bearer ***API*KEY***' -H 'Content-Type: application/json' http://127.0.0.1:9000/api/case/template -d '{
  "name":"My first template",
  "titlePrefix":"test",
  "severity":2,
  "tlp":2, 
  "pap":2,
  "tags":[],
  "tasks":[],
  "metrics":{},
  "customFields":{},
  "description":"This is my first template"
  }'
```
