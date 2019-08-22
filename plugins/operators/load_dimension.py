from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 # Example:
                 # conn_id = your-connection-name
                 redshift_conn_id = 'redshift',
                 dim_sql = '',
                 delete_sql = '',
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        self.redshift_conn_id = redshift_conn_id
        self.dim_sql = dim_sql
        self.delete_sql = delete_sql 

    def execute(self, context):
        self.hook =  PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info('Executing LoadDimOperator ......')
        if self.delete_sql != '':
            self.log.info('Executing Delete Operator ......')
            self.hook.run(self.delete_sql)
            self.log.info('Completing Delete Operator ......')
        self.hook.run(self.dim_sql)
        self.log.info('Completing LoadDimOperator ......')
