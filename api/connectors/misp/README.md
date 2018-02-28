# MISP connector

MISP and TheHive can interact between each other in both ways:
* TheHive is able to import events from a MISP instance as alerts and create cases from them
* TheHive is able to export a case into MISP as an event and update it with the artifacts flagged as IOC as MISP attributes

It is possible to use the API to control those behaviours.

## MISP imports

### API methods

| HTTP Method | URI                                | Action                                                                                        |
|-------------|------------------------------------|-----------------------------------------------------------------------------------------------|
| GET         | /api/connector/misp/_syncAlerts    | Synchronize from all MISP instances all MISP events published since the last synchronization  |
| GET         | /api/connector/misp/_syncAllAlerts | Synchronize from all MISP instances all MISP published events since the beginning             |
| GET         | /api/connector/misp/_syncArtifacts | Synchronize all artifacts from already imported alerts from all MISP instances                |

## MISP exports

### API methods

| HTTP Method | URI                                           | Action                |
|-------------|-----------------------------------------------|-----------------------|
| POST        | /api/connector/misp/export/:caseId/:mispName | Export a case to MISP |

### Exporting a case to MISP
Exporting a case to MISP can be done by performing the following query
```
POST /api/connector/misp/export/:caseId/:mispName
```
With:
* caseId: the _elasticsearch_ id of the case
* mispName: the name given to the MISP instance in TheHive configuration

No parameters need to be sent in the query body.

The response of this query will be a JSON table containing all artifacts sent as attributes in the MISP event.
