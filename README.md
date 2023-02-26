# Data Engineering Nanodegree Capstone Project

This repository serves as a submission for Udacity's data engineer nanodegree.

## Project Introduction
In this project we are working with movie data from [IMDB](https://www.imdb.com/interfaces/).
The goal is to build an ETL pipeline which creates a mini data warehouse that can be used for movie analytics.
The immediate questions we want to answer are:
- Which actor/actress has the highest movie rating average?
- which actor/actress has been in most high rated movies?
- Do actors or acctresses have a better average movie rating in different types of titles productions (movie, series, video game, etc.)?

## Next steps (remove this section before submitting)
- add analytical view creation
- remove Empty & final run
- prepare README
- read udacity instructions again and patch up the project
- finalise readme

## Prerequisites

**Install python requirements**
```
pip install -r requirements.txt
```

**Pull the Data**
```
python scripts/get_data.py
```

**Setup Airflow**
```
# if on a unix machine run below
# echo -e "AIRFLOW_UID=$(id -u)" > .env

mkdir -p ./dags ./logs ./plugins 
docker-compose up airflow-init
docker-compose up
# to run commands in the container
# docker exec <process id> airflow version 

# shutdown airflow
docker-compose down
```
Access Airflow here: http://localhost:8080/

**Create Airflow Connection**
To run this project you will need to create a connection in Airflow UI.
The connection to the DW (data warehouse - postgres db).
- conn id: postgresdw
- conn type: postgres
- username: postgres
- password: postgres
- host: postgres-dw (if running via the included docker-compose.yaml)
- port 5432 (becuase both airflow and the dw are on docker, else you need 5431)

**Connect to Data Warehouse**
The docker-compose file will also start up a postgres db.
That is the db we are connecting to with above connection.
It maps port 5432 to 5431 on your machine, so connect to it as below.
```
psql -h 127.0.0.1 -p 5431 -U postgres
# username: postgres
# password: postgres
```

## How to Run?

This section describes how to get use this repositrory.

**Initialize the database**
To initialize the db we need to run the imdb_init dag in the airflow UI.
http://localhost:8080/
The DAG will create 4 staging tables and 3 live tables.

**Run the ETL**


## Project Structure
```
\dags --> holds airflow DAGS
\plugins --> holds Airflow plugins (custom operators, etc.)
\notebooks --> experimental code and data exploration
\scripts --> scripts to help with dev and setup
```
