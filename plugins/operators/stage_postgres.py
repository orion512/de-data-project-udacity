import os
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class StageToPostgresOperator(BaseOperator):
    """ Custom operator for staging data from CSV to Postgres """
    ui_color = '#f5cd40' # imdb #f5c518
    copy_sql = """
        COPY {}
        FROM STDIN
        DELIMITER {} QUOTE {}
        CSV HEADER
    """

    @apply_defaults
    def __init__(self,
        table_name,
        file_path,
        delimiter,
        pg_conn_id,
        quote="E'\b'",
        *args, **kwargs):

        super(StageToPostgresOperator, self).__init__(*args, **kwargs)
        self.table_name = table_name
        self.file_path = file_path
        self.delimiter = delimiter
        self.pg_conn_id = pg_conn_id
        self.quote = quote

    def execute(self, context):
        """ reads file and writes it to a table in postgres """

        self.log.info('StageToPostgresOperator starting')
        pg_hook = PostgresHook(postgres_conn_id=self.pg_conn_id)

        self.log.info("Clearing data from destination Postgres table")
        pg_hook.run("DELETE FROM {}".format(self.table_name))

        # if file does not exsist -> error (copy_expert doesn't check)
        if not os.path.exists(self.file_path):
            raise(FileNotFoundError(f"File {self.file_path} doesn't exist!"))

        # sql_temp = "COPY st_title_basics FROM STDIN DELIMITER E'\t' QUOTE E'\b' CSV HEADER"

        self.log.info("Copying data from file to Postgres")
        formatted_sql = self.copy_sql.format(
            self.table_name, self.delimiter, self.quote)
        pg_hook.copy_expert(formatted_sql, self.file_path)

        self.log.info(f'StageToPostgresOperator finished')
