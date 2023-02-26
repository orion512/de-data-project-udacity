from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class CreateViewOperator(BaseOperator):
    """ Custom operator for creating views """

    sql_view = 'create or replace VIEW {} as {}'

    @apply_defaults
    def __init__(self,
                 pg_conn_id="",
                 view_name="",
                 view_sql="",
                 *args, **kwargs):

        super(CreateViewOperator, self).__init__(*args, **kwargs)
        self.pg_conn_id = pg_conn_id
        self.view_name = view_name
        self.view_sql = view_sql

    def execute(self, context):
        """ create view from provided sql """
        self.log.info(f'CreateViewOperator starting: {self.view_name}')

        pg_hook = PostgresHook(postgres_conn_id=self.pg_conn_id)

        sql_stmt = CreateViewOperator.sql_view.format(self.view_name, self.view_sql)

        pg_hook.run(sql_stmt)

        self.log.info('CreateViewOperator done')
