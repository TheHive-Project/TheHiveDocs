# Task

## Model definition

Required attributes:
 - `title` (text) : title of the task
 - `status` (taskStatus) : status of the task (*Waiting*, *InProgress*, *Completed* or *Cancel*) **default=Waiting**
 - `flag` (boolean) : flag of the task **default=false**

Optional attributes:
 - `owner` (string) : user who owns the task. This is automatically set to current user when status is set to
 *InProgress*
 - `description` (text) : task details
 - `startDate` (date) : date of the beginning of the task. This is automatically set when status is set to *Open*
 - `endDate` (date) : date of the end of the task. This is automatically set when status is set to *Completed*

## Task manipulation

### Task methods

|HTTP Method |URI                                     |Action                                |
|------------|----------------------------------------|--------------------------------------|
|POST        |/api/case/:caseId/task/_search          |Find tasks in a case (deprecated)     |
|POST        |/api/case/task/_search                  |Find tasks                            |
|POST        |/api/case/task/_stats                   |Compute stats on tasks                |
|GET         |/api/case/task/:taskId                  |Get a task                            |
|PATCH       |/api/case/task/:taskId                  |Update a task                         |
|POST        |/api/case/:caseId/task                  |[Create a task](#create-a-task)       |

### Create a task
The URL used to create a task is:
```
POST /api/case/<<caseId>>/task
```
\<\<caseId\>\> must be replaced by case id (not the case number !)

Required task attributes (cf. models) must be provided.

This call returns attributes of the created task.

#### Examples
Creation of a simple task in case `AVqqdpY2yQ6w1DNC8aDh`:
```
curl -XPOST -H 'Authorization: Bearer ***API*KEY***' -H 'Content-Type: application/json' http://127.0.0.1:9000/api/case/AVqqdpY2yQ6w1DNC8aDh/task -d '{
  "title": "Do something"
}'
```
It returns:
```
{
  "createdAt": 1488918771513,
  "status": "Waiting",
  "createdBy": "myuser",
  "title": "Do something",
  "order": 0,
  "user": "myuser",
  "flag": false,
  "id":"AVqqeXc9yQ6w1DNC8aDj",
  "_id":"AVqqeXc9yQ6w1DNC8aDj",
  "_type":"case_task"
}
```

Creation of another task:
```
curl -XPOST -H 'Authorization: Bearer ***API*KEY***' -H 'Content-Type: application/json' http://127.0.0.1:9000/api/case/AVqqdpY2yQ6w1DNC8aDh/task -d '{
  "title": "Analyze the malware",
  "description": "The malware XXX is analyzed using sandbox ...",
  "owner": "Joe",
  "status": "InProgress"
}'
```
