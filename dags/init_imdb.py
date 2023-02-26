import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from utils import SqlQueriesInit

default_args = {
    'owner': 'Dominik Zulovec Sajovic',
    'start_date': datetime(2023, 1, 1),
    'depends_on_past': False,
    'email_on_retry': False,
}

dag = DAG(
    'imdb_init',
    default_args=default_args,
    description='Initialize the Imdb database',
    schedule_interval=None,
    catchup=False,
)

start_operator = EmptyOperator(task_id='begin_execution',  dag=dag)

st_title_basics_create = PostgresOperator(
    task_id='st_title_basics_create',
    postgres_conn_id="postgresdw",
    sql=SqlQueriesInit.st_title_basics_create,
    dag=dag
)

st_title_ratings_create = PostgresOperator(
    task_id='st_title_ratings_create',
    postgres_conn_id="postgresdw",
    sql=SqlQueriesInit.st_title_ratings_create,
    dag=dag
)

st_title_principals_create = PostgresOperator(
    task_id='st_title_principals_create',
    postgres_conn_id="postgresdw",
    sql=SqlQueriesInit.st_title_principals_create,
    dag=dag
)

st_name_basics_create = PostgresOperator(
    task_id='st_name_basics_create',
    postgres_conn_id="postgresdw",
    sql=SqlQueriesInit.st_name_basics_create,
    dag=dag
)

init_live_tables = EmptyOperator(task_id='init_live_tables',  dag=dag)

title_create = PostgresOperator(
    task_id='title_create',
    postgres_conn_id="postgresdw",
    sql=SqlQueriesInit.title_create,
    dag=dag
)

casting_create = PostgresOperator(
    task_id='casting_create',
    postgres_conn_id="postgresdw",
    sql=SqlQueriesInit.casting_create,
    dag=dag
)

person_create = PostgresOperator(
    task_id='person_create',
    postgres_conn_id="postgresdw",
    sql=SqlQueriesInit.person_create,
    dag=dag
)

end_operator = EmptyOperator(task_id='end_execution',  dag=dag)

####################
## Pipeline Order ##
####################

start_operator >> [
    st_title_basics_create,
    st_title_ratings_create,
    st_title_principals_create,
    st_name_basics_create,
] >> init_live_tables

init_live_tables >> [
    title_create,
    casting_create,
    person_create,
] >> end_operator
