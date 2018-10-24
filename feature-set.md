# Feature set

This document will list the features provided by TheHive either from the UI or using APIs and Webhooks.

TheHive comes with the native support of integrating:

- one or multiple Cortex instances
- one or multiple MISP instances

## Authentication

TheHive supports multiple authentication methods:

- Local authentication using a local user collection
- AD authentication
- LDAP authentication
- SSO authentication
- X.509 certificates authentication

## Case Management

- List and filter cases
- Create new cases from scratch or using case templates
- Add custom fields to cases
- Add metrics to cases
- Find linked cases to a given case based shared observables
- Add tasks and task groups to cases
- Assign tasks to a given user
- Add logs to tasks, including attachment to task logs
- Add observables to a case
- Execute Cortex responders against
  - cases
  - tasks
  - task logs
- Delete cases by administrators only

## Alert Management

Alerts are a sort of incidents not yet qualified as a Case. The Alerts sections allows:

- Listing and searching for alerts
- Marking alerts read
- Ignoring alerts update
- Previewing alert details
  - Display alert details and editable custom fields
  - Display alert's observables
  - Display similar cases
- Importing an alert as an emtpty case or using a case template
- Merging an alert into an existing case

### MISP Integration

MISP is natively integrated to TheHive allowing:

- Declaring one or multiple MISP instances
- Each instance can be used to Import and/or Export events from MISP or cases to MISP
- Imported MISP events are made available as Alerts
- Imporing is configurable using filters (configuration files)

### Feeders

- Feeders are external tools designed to send alerts to TheHive leveraging the REST APIs Thehive offers
- Feeders can be written and any programming language as long as they can play with TheHive APIs
- Feeders can be written in Python and use TheHive4Py

## Search capabilities

The search section provided by TheHive allows searching for the following objects using dynamic forms:

- cases
- tasks
- observables
- logs
- alerts

## Dashboarding

The dashboards section allows:

- creating private dashboards per user
- creating shared dashboads visible by all users
- adding widgets to dashboards using a drag & drop capabilities
- creating widgets that target cases, tasks, observables, alerts, jobs
- configuring widgets in a granular manner

## Administration

### Case templates

- Create case templates
- Add tasks to templates
- Add metrics to templates
- Add custom fields to templates
- Define default values for custom fields, metrics and tasks
- Export case template definitions
- Import case template definitions

### Metrics

- List and Create metrics

### Custom fields

- Create custom fields
- Update custom fields

### Users

- List users
- Create/Edit users
- Set a user password
- Set a user API key
- Revoke a user's API key
- Lock a user

### Analyzer report templates

Report templates are used to display the raw reports from Cortex in a human readable format. This section allows:

- Importing short and long reports
- Customize short and long reports for each analyzer

## Cortex integration

TheHive uses Cortex to have access to analyzers and responsders

- Analyzers can be launched against observables to get more details about a given observable
- Responders can be launched against case, tasks, observables, logs, and alerts to execute an action
- One or multiple Cortex instances can be connected to TheHive

## Database migration

TheHive provides a mechanism to upgrade the Elasticsearch database by copying the index and making transformations on it.