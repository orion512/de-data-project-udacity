# Data Engineering Nanodegree Capstone Project

This repository serves as a submission for Udacity's data engineer nanodegree.

## Project Introduction
In this project we are working with movie data from [IMDB](https://www.imdb.com/interfaces/).
The goal is to build an ETL pipeline which creates a mini data warehouse that can be used for movie analytics.
The immediate question we want to answer are:
- Which actor/actress has the highest movie rating average?
- which actor/actress has been in most high rated movies?
- Average of actors/actresses in different types of media productions (movie, series, video game, etc.)

## Prerequisites

```
# if on a unix machine run below
# echo -e "AIRFLOW_UID=$(id -u)" > .env

mkdir -p ./dags ./logs ./plugins
python scripts/get_data.py
docker-compose up airflow-init
docker-compose up
# docker exec <process id> airflow version 

access airflow
http://localhost:8080/

connect to Postgres DW
psql -h 127.0.0.1 -p 5431 -U postgres
```

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
