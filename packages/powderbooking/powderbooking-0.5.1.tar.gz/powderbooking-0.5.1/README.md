# powderbooking-database
Database model for the Powderbooking application

## How to use
This database model is pushed to pypi to make it available for all microservices.

This package uses [Poetry](https://python-poetry.org/) to maintain dependencies and to push to pypi.

## Environmental variables

To use this package to create the database connection, the following environmental variables need to be set.

| name  | optional  | description |
|---|---|---|
|PROJECT_NAME   | false   | The name of the project, that is used by kubernetes to indicate service port and host.  |
|POSTGRESQL_USER   | false   | the username  |
|POSTGRESQL_PASSWORD   | false   | the password  |
|{PROJECT_NAME}_POSTGRESQL_SERVICE_HOST   | false   | host of postgresql  |
|{PROJECT_NAME}_POSTGRESQL_SERVICE_PORT   | false   | port of postgresql  |
|POSTGRESQL_DATABASE   | false   | the database that is used  |