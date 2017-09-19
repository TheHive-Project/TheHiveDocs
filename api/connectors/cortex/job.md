# Job

## Model definition

Required attributes:
- `analyzerId` (string): identifier of the analyzer used by the job
- `status` (enumeration): status of the job (`InProgress`, `Success`, `Failure`) **default=`InProgress`**
- `artifactId` (string): identifier of the artifact to analyze
- `startDate` (date): job start date

Optional attributes:
- `endDate` (date): job end date
- `report` (string): raw content of the report sent back by the analyzer
- `cortexId` (string): identifier of the cortex server
- `cortexJobId` (string): identifier of the job in the cortex server

## Job manipulation

### Job methods

| HTTP Method |URI                                |Action                   |
|-------------|-----------------------------------|-------------------------|
|POST         | /api/connector/cortex/job         | Create a new Cortex job |
|GET          | /api/connector/cortex/job/:jobId  | Get a cortex job        |
|POST         | /api/connector/cortex/job/_search | Search for cortex jobs  |

### Create a new Cortex job
Creating a new job can be done by performing the following query
```
POST  /api/connector/cortex/job
```
Parameters:
- `cortexId`: identifier of the Cortex server
- `artifactId`: identifier of the artifact as found with an artifact search
- `analyzerId`: name of the analyzer used by the job
