import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from operators import (
    StageToPostgresOperator
    # LoadFactOperator, LoadDimensionOperator, DataQualityOperator
    )
from utils import SqlQueries

default_args = {
    'owner': 'Dominik Zulovec Sajovic',
    'start_date': datetime(2023, 1, 1),
    'depends_on_past': False,
    'email_on_retry': False,
}

dag = DAG(
    'imdb_dag',
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

# load_songplays_table = LoadFactOperator(
#     task_id='Load_songplays_fact_table',
#     redshift_conn_id="redshift",
#     select_sql=SqlQueries.songplay_table_insert,
#     dest_table="songplays",
#     dag=dag
# )

# load_user_dimension_table = LoadDimensionOperator(
#     task_id='Load_user_dim_table',
#     redshift_conn_id="redshift",
#     select_sql=SqlQueries.user_table_insert,
#     dest_table="users",
#     truncate=True,
#     dag=dag
# )

# load_song_dimension_table = LoadDimensionOperator(
#     task_id='Load_song_dim_table',
#     redshift_conn_id="redshift",
#     select_sql=SqlQueries.song_table_insert,
#     dest_table="songs",
#     truncate=True,
#     dag=dag
# )

# load_artist_dimension_table = LoadDimensionOperator(
#     task_id='Load_artist_dim_table',
#     redshift_conn_id="redshift",
#     select_sql=SqlQueries.artist_table_insert,
#     dest_table="artists",
#     truncate=True,
#     dag=dag
# )

# load_time_dimension_table = LoadDimensionOperator(
#     task_id='Load_time_dim_table',
#     redshift_conn_id="redshift",
#     select_sql=SqlQueries.time_table_insert,
#     dest_table="time",
#     truncate=True,
#     dag=dag
# )

# run_quality_checks = DataQualityOperator(
#     task_id='Run_data_quality_checks',
#     redshift_conn_id="redshift",
#     table_name="time",
#     dag=dag
# )

end_operator = EmptyOperator(task_id='end_execution',  dag=dag)

start_operator >> stage_title_basics_to_postgres
start_operator >> stage_title_ratings_to_postgres
start_operator >> stage_title_principals_to_postgres
start_operator >> stage_name_basics_to_postgres

stage_title_basics_to_postgres >> end_operator
stage_title_ratings_to_postgres >> end_operator
stage_title_principals_to_postgres >> end_operator
stage_name_basics_to_postgres >> end_operator