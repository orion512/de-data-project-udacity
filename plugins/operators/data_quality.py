from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    """ Custom operator for data quality """

    ui_color = '#89DA59'
    sql_check = 'SELECT COUNT(*) FROM {}'

    @apply_defaults
    def __init__(self,
                 pg_conn_id="",
                 table_name="",
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.pg_conn_id = pg_conn_id
        self.table_name = table_name

    def execute(self, context):
        """ Checks if the table has more than 0 rows """
        self.log.info('DataQualityOperator starting')

        redshift = PostgresHook(postgres_conn_id=self.pg_conn_id)

        sql_stmt = DataQualityOperator.sql_check.format(self.table_name)

        records = redshift.get_records(sql_stmt)

        if len(records) < 1 or len(records[0]) < 1:
            raise ValueError(f"Table {self.table_name} returned no results")

        if records[0][0] < 1:
            raise ValueError(f"Table {self.table_name} has 0 rows")

        self.log.info('DataQualityOperator done')