# Observable

## Model definition

Required attributes:

 - `data` (string) : content of the observable (read only). An observable can't contain data and attachment attributes
 - `attachment` (attachment) : observable file content (read-only). An observable can't contain data and attachment
 attributes
 - `dataType` (enumeration) : type of the observable (read only)
 - `message` (text) : description of the observable in the context of the case
 - `startDate` (date) : date of the observable creation **default=now**
 - `tlp` (number) : [TLP](https://www.us-cert.gov/tlp) (`0`: `white`; `1`: `green`; `2`: `amber`;
 `3`: `red`) **default=2**
 - `ioc` (boolean) : indicates if the observable is an IOC **default=false**
 - `status` (artifactStatus) : status of the observable (*Ok* or *Deleted*) **default=Ok**

Optional attributes:
 - `tags` (multi-string) : observable tags
 
## Observable manipulation

### Observable methods

|HTTP Method |URI                                     |Action                                |
|------------|----------------------------------------|--------------------------------------|
|POST        |/api/case/artifact/_search              |Find observables                      |
|POST        |/api/case/artifact/_stats               |Compute stats on observables          |
|POST        |/api/case/:caseId/artifact              |Create an observable                  |
|GET         |/api/case/artifact/:artifactId          |Get an observable                     |
|DELETE      |/api/case/artifact/:artifactId          |Remove an observable                  |
|PATCH       |/api/case/artifact/:artifactId          |Update an observable                  |
|GET         |/api/case/artifact/:artifactId/similar  |Get list of similar observables       |
|PATCH       |/api/case/artifact/_bulk                |Update observables in bulk            |

### List Observables of a Case
Complete observable list of a case can be retrieved by performing a search:
```
POST     /api/case/artifact/_search
```
Parameters:
 - `query`: `{ "_parent": { "_type": "case", "_query": { "_id": "<<caseId>>" } } }`
 - `range`: `all`

\<\<caseId\>\> must be replaced by case id (not the case number !)

