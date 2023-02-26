# Data Engineering Nanodegree Capstone Project

This repository serves as a submission for Udacity's data engineer nanodegree.

## Project Introduction
In this project we are working with movie data from [IMDB](https://www.imdb.com/interfaces/).
The goal is to build an ETL pipeline which creates a mini data warehouse that can be used for movie analytics.
The immediate questions we want to answer are:
- Which actor/actress has the highest movie rating average?
- which actor/actress has been in most high rated movies?
- Do actors or acctresses have a better average movie rating in different types of titles productions (movie, series, video game, etc.)?

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
- schema: dw
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
Now we can run the main DAG - imdb_etl.
It can take some time (15-25 min) depending on the executor setup and the resources available.
When it finishes running we have:
- 4 stageing tables (all fields as TEXT)
- 3 live loaded tables
- 3 analytical views

## Project Structure
```
\dags --> holds airflow DAGS
\plugins --> holds Airflow plugins (custom operators, etc.)
\notebooks --> experimental code and data exploration
\scripts --> scripts to help with dev and setup
```

## Project Write-Up

The goal of this project as mentioned in the introduction section is to create a data warehouse with data about movies, their ratings and all the personnel involved in making movies.
By the end we want to be able to run queries which answer the below questions:
- Which actor/actress has the highest movie rating average?
- which actor/actress has been in most high rated movies?
- Do actors or acctresses have a better average movie rating in different types of titles productions (movie, series, video game, etc.)?

The entire project/pipeline is implemented using Airflow which makes it clear and simple to follow run and observe what is happening. The instructions on how to setup and run the pipeline can be found in the beginning of this file.
While the project in its current state doesn't make use of Big Data technologies such as Spark this could be incroporeted through AWS clusters (AWS MWAA and/or EMR).

### Data

As mentioned before the data for the project comes from [IMDB](https://www.imdb.com/interfaces/).
The raw data is available on a tabular format (TSV files) and i choose 4 files from the link which I wanted to use:
- name.basics (information about people)
- title.basics (information about movies)
- title.principals (information about people acting in movies)
- title.ratings (information about movie ratings)

The data already came nicely organised and fairly suited for a data warehouse. It wasn't too normalised neither too denormalised.
Steps I took to get to my final data model.

- name.basics contained information about people and so I decided to rename it to "person" and use it as one of my Dimension tables.
- title.basics and title.ratings both contained information about movies (and other types of titles) and so i decided to combine them (denormalise further) and call the "title". This was my next Dimension table.
- the final file (title.principals) containes data combining both "person" and "title" table.
I decided to rename it into "casting" and this was now my Fact table.

And so the final data model looks something like below.
1 and * indicating a one-many connection.

```
title
+---------------+
| tconst        |
| titleType     |
| primaryTitle  |
| originalTitle |
| isAdult       |
| startYear     |
| endYear       |
| runtimeMinutes|
| genres        |
| averageRating |
| numVotes      |
+---------------+
         |
         | 1
         +
         | *
         |
casting                       
+---------------+
| id            |
| tconst        |
| ordering      |
| nconst        |
| category      |
| job           |
| characters    |
+---------------+
         |
         | *
         +
         | 1
         |
person
+---------------+
| nconst        |
| primaryName   |
| birthYear     |
| deathYear     |
| primaryProfession|
| knownForTitles|
+---------------+
```

This data model allows me to execute the qeuries I need to answer my questions.
by joining titler and rating togther I don't sacrifice any extra space and don't need to write extra joins when writing my analytical queries.

The data should be updated daily as is stated on the IMDB website. Theyu update the data daily and so this datasets should follow the same schedule to keep it up to date.
The data download process in is not a part of the airflow dag and so that would have to be either added or scheduled separately. However the SQL queries are already written in a way to insert any new data and update any old records.

### Steps
1. Choosing tha data
I started this project by exploring some free datasets online which match the size criteria for this project. IMDB was fiot for puropose and interesting to me
2. To explore the datasets I used a Jupyter notebook as it is a very powerful to and very fast when working with a limited number of data rows. The exploration helped me to understand where we had missing values adn other properties of the data.
3. When the exploration was done I was able to create a data model as described in the previous section.
4. Staging the data; the next step was to write an airflow operator which could stage my TSV files into the staging area of the database. All the tables in the staging area have columns of type TEXT. This so that I can easily load all the files into SQL and then use SQL queries to convert columns as I see fit.
5. Now that I had all the data within SQL tables I was able to write my load SQL queries to convert the columns and write them into live tables.
6. Data quality came next where i executed a 0 rows checker for each of the live tables.
7. And finally we wanted to answer our analytical qustions. For this step I wrote SQL queries which were able to provide the answers and then used them to create views.


### Tools
- Airflow is used for the pipeline orchestration; Could use some other tool like Dagster or Mage however I wanted to use Airflow as it was used throughout this course.
- AS the data I used was in a tabular structured format (TSV files) I decided to use postgresSQl database.

### Scenarios

**If the data was increased by 100x**
In this case I would start by replacing the the raw PostgreSQl database with a columnar version such as redshift. Additonally I would run Redshift on spark clusters.
it would also be worth to consider a move to a noSQl databse such as mongoDB or Cassandra.

**If the pipelines were run on a daily basis by 7am**
The pipelines are meant to run on a daily basis. If the pipelines would be taking too long we could make use of distributed computing. it might beworth taking a more data lake approach instead of a data warehouse approach and keep some files on S3 while some smaller subsets would make it to the SQL database.

**If the database needed to be accessed by 100+ people**
In this case it would be goo to make use of partitioning to split the large tables into smaller subtables. This can improve query performance and maintenance operations by reducing the amount of data scanned or modified.
We would also have to make sure to setup proper indexes on tables (by making educated guesses on the types of queries we will be running).
Killing long running queries in order to now slow down other queries.

### Analytics Results
Here are some short answers to the main questions we wanted to answer.
It is worth saying that we excluded all the movies (titles) with less than 5k votes.

**Which actor/actress has the highest movie rating average?**
To answer this question we considered only actors who's movies have a gotten at least 5 Million votes thropughout their acting career.
1. Leonardo DiCaprio 7.41
2. Ken Watanabe	7.38
3. Rupert Grint	7.17
4. Ian McKellen	7.10
5. Brad Pitt	7.10

**which actor/actress has been in most high rated movies?**
A high rated movie is a movie with at least a rate of 8.5.
1. Kemal Sunal 10
2. Sener Sen 9
3. Adile Nasit 8
4. Mohanlal	6
5. Münir Özkul 6
...
10. Orlando Bloom 3

**Do actors or acctresses have a better average movie rating in different types of titles productions (movie, series, video game, etc.)?**
Actors appear in titles with a higher average rating then actresses in nearly every category.
The only 2 categories (title types) where actresses appear in higher rated titles are: TV Specials and Video Games.
