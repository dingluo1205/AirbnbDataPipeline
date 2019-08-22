from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.S3_hook import S3Hook

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    
    copy_query = """
            COPY {}
            FROM ''
            with credentials
            'aws_access_key_id={};aws_secret_access_key={}'
            region 'us-west-2';
            """
 
    @apply_defaults
    def __init__(self,
                 # Define operators params (with defaults) here
                 table = '',
                 s3_path = '',
                 conn_id = 'aws_credentials',
                 redshift_conn_id = 'redshift',
                 autocommit = True,
                 verify = None,
                 copy_options = '',
                 *args, **kwargs):
        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        # Map params here
        self.conn_id = conn_id
        self.redshift_conn_id = redshift_conn_id
        self.table = table 
        self.s3_path = s3_path 
        self.autocommit = autocommit
        self.copy_options = copy_options
        self.verify = verify
      

    def execute(self, context):
        self.hook =  PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.s3 = S3Hook(aws_conn_id=self.conn_id, verify=self.verify)
        credentials = self.s3.get_credentials()
        #copy_options = '\n\t\t\t'.join(self.copy_options)
        
        ## stage either s3 files or gzip s3 files to redshift 
        ## need to remove null value, add delimiter, and ignore header 
        if self.copy_options == 'gzip':
            copy_query = """
            COPY {table}
            FROM '{s3_path}'
            with credentials
            'aws_access_key_id={access_key};aws_secret_access_key={secret_key}'
            NULL AS 'NULL'
            EMPTYASNULL
            TRIMBLANKS TRUNCATECOLUMNS ACCEPTINVCHARS dateformat as 'auto' GZIP csv quote as '"' 
            delimiter ',' IGNOREHEADER as 1 MAXERROR as 10000;
            ;
        """.format(table=self.table,
                   s3_path=self.s3_path,
                   access_key=credentials.access_key,
                   secret_key=credentials.secret_key)
        else:
            copy_query = """
            COPY {table}
            FROM '{s3_path}'
            with credentials
            'aws_access_key_id={access_key};aws_secret_access_key={secret_key}'
            csv 
            NULL AS 'NULL'
            EMPTYASNULL
            delimiter ',' 
            IGNOREHEADER 1
            ;
        """.format(table=self.table,
                   s3_path=self.s3_path,
                   access_key=credentials.access_key,
                   secret_key=credentials.secret_key)

        self.log.info('Executing COPY command...')
        self.hook.run(copy_query, self.autocommit)
        self.log.info("COPY command complete...")





