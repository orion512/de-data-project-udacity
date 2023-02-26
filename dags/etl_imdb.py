from datetime import datetime
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from operators import (
    StageToPostgresOperator,
    DataQualityOperator,
    CreateViewOperator,
)
from utils import SqlQueriesLoad, SqlQueriesAnalytics

default_args = {
    'owner': 'Dominik Zulovec Sajovic',
    'start_date': datetime(2023, 1, 1),
    'depends_on_past': False,
    'email_on_retry': False,
}

dag = DAG(
    'imdb_etl',
    default_args=default_args,
    description='Load and transform imdb data.',
    schedule_interval='@daily',
    catchup=False,
)

start_operator = EmptyOperator(task_id='begin_execution',  dag=dag)

stage_title_basics_to_postgres = StageToPostgresOperator(
    task_id='stage_title_basics',
    table_name="st_title_basics",
    file_path='/opt/datasets/title.basics.tsv',
    delimiter="E'\t'",
    pg_conn_id="postgresdw",
    dag=dag,
)

stage_title_ratings_to_postgres = StageToPostgresOperator(
    task_id='stage_title_ratings',
    table_name="st_title_ratings",
    file_path='/opt/datasets/title.ratings.tsv',
    delimiter="E'\t'",
    pg_conn_id="postgresdw",
    dag=dag,
)

stage_title_principals_to_postgres = StageToPostgresOperator(
    task_id='stage_title_principals',
    table_name="st_title_principals",
    file_path='/opt/datasets/title.principals.tsv',
    delimiter="E'\t'",
    pg_conn_id="postgresdw",
    dag=dag,
)

stage_name_basics_to_postgres = StageToPostgresOperator(
    task_id='stage_name_basics',
    table_name="st_name_basics",
    file_path='/opt/datasets/name.basics.tsv',
    delimiter="E'\t'",
    pg_conn_id="postgresdw",
    dag=dag,
)

start_load_operator = EmptyOperator(task_id='loading_begin',  dag=dag)

load_casting_table = PostgresOperator(
    task_id='load_casting_fact_table',
    postgres_conn_id="postgresdw",
    sql=SqlQueriesLoad.casting_insert,
    dag=dag
)

load_person_table = PostgresOperator(
    task_id='load_person_dim_table',
    postgres_conn_id="postgresdw",
    sql=SqlQueriesLoad.person_insert,
    dag=dag
)

load_title_table = PostgresOperator(
    task_id='load_title_dim_table',
    postgres_conn_id="postgresdw",
    sql=SqlQueriesLoad.title_insert,
    dag=dag
)

start_quality = EmptyOperator(task_id='start_quality',  dag=dag)

run_quality_title = DataQualityOperator(
    task_id='run_quality_title',
    pg_conn_id="postgresdw",
    table_name="title",
    dag=dag
)

run_quality_person = DataQualityOperator(
    task_id='run_quality_person',
    pg_conn_id="postgresdw",
    table_name="person",
    dag=dag
)

run_quality_casting = DataQualityOperator(
    task_id='run_quality_casting',
    pg_conn_id="postgresdw",
    table_name="casting",
    dag=dag
)

start_analytics = EmptyOperator(task_id='start_analytics',  dag=dag)

actors_avgs_analytics = CreateViewOperator(
    task_id='actors_avgs_analytics',
    pg_conn_id="postgresdw",
    view_name="actors_best_avg",
    view_sql=SqlQueriesAnalytics.actors_avg_rating,
    dag=dag
)

actors_high_movies_analytics = CreateViewOperator(
    task_id='actors_high_movies_analytics',
    pg_conn_id="postgresdw",
    view_name="actors_high_rated_movies",
    view_sql=SqlQueriesAnalytics.actors_high_rated_movies,
    dag=dag
)

actors_actresses_analytics = CreateViewOperator(
    task_id='actors_actresses_analytics',
    pg_conn_id="postgresdw",
    view_name="actors_actresses_scores",
    view_sql=SqlQueriesAnalytics.actors_actresses,
    dag=dag
)

end_operator = EmptyOperator(task_id='end_execution',  dag=dag)

####################
## Pipeline Order ##
####################

start_operator >> [
    stage_title_basics_to_postgres,
    stage_title_ratings_to_postgres,
    stage_title_principals_to_postgres,
    stage_name_basics_to_postgres,
] >> start_load_operator

start_load_operator >> [
    load_casting_table,
    load_person_table,
    load_title_table,
] >> start_quality

start_quality >> [
    run_quality_title,
    run_quality_person,
    run_quality_casting,
] >> start_analytics

start_analytics >> [
    actors_avgs_analytics,
    actors_high_movies_analytics,
    actors_actresses_analytics,
] >> end_operator
