# Data Pipelines with Airflow

This repository serves as a submission for Udacity data engineer nanodegree.

## Project Introduction
A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.

This project reads data from an already existing S3 bucket and moves it into a Postgres (Redshift) database.
After it performs further transformations on the Redshift DB itself.

## How to Run?

This section describes how to get use this repositrory.

**Create Airflow Connections**
To run this project you will need two connections in airflow.
- redshift database
- Amazon Web Services

**Initialize the database**
before starting you will also need to run the create_tables.sql on your
Redshift database.

**Run airflow with Docker (optional)**
If you want to setup the airflow environemnt through docker.
```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.5.0/docker-compose.yaml'
```
Then use below commands to setup the container
```
# initialize
docker-compose up airflow-init
# start
docker-compose up
# stop
docker-compose down

# to run commands in the container
# docker exec <process id> airflow version 
```

## Project Structure
```
\dags --> holds airflow DAGS
\logs --> for airflow logs
\plugins --> holds Airflow plugins (custom operators, etc.)
```
