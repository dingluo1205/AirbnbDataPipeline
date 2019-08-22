from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

# AWS_KEY = os.environ.get('AWS_KEY')
# AWS_SECRET = os.environ.get('AWS_SECRET')

default_args = {
    'owner': 'dingluo',
    'start_date': datetime(2019, 1, 12),
    'retries': 1,
    'depends_on_past': False,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG('airbnb_dag',
          default_args=default_args,
          catchup=False,
          description='Load and transform airbnb data in Redshift with Airflow',
          schedule_interval='0 0 0 * *'
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

stage_reviews_to_redshift = StageToRedshiftOperator(
    task_id='Stage_reviews',
    dag=dag,
    table = 'staging_reviews',
    s3_path = 's3://airbnb-capstone/reviews',
    conn_id = 'aws_credentials',
    redshift_conn_id = 'redshift',
    copy_options = 'gzip'
)

stage_listings_to_redshift = StageToRedshiftOperator(
    task_id='Stage_listings',
    dag=dag,
    table = 'staging_listings',
    s3_path = 's3://airbnb-capstone/listings',
    conn_id = 'aws_credentials',
    redshift_conn_id = 'redshift',
    copy_options = 'csv'
)

stage_calendar_to_redshift = StageToRedshiftOperator(
    task_id='Stage_calendar',
    dag=dag,
    table = 'staging_calendar',
    s3_path = 's3://airbnb-capstone/calendar',
    conn_id = 'aws_credentials',
    redshift_conn_id = 'redshift',
    copy_options = 'gzip'
)

load_review_table = LoadFactOperator(
    task_id='Load_review_fact_table',
    dag=dag,
    redshift_conn_id = 'redshift',
    fact_sql = SqlQueries.review_table_insert
    # if you want to delete the table first, please uncomment this one 
    # delete_sql = SqlQueries.review_table_delete 
)

load_calendar_table = LoadFactOperator(
    task_id='Load_calendar_fact_table',
    dag=dag,
    redshift_conn_id = 'redshift',
    fact_sql = SqlQueries.calendar_table_insert
    # if you want to delete the table first, please uncomment this one 
    # delete_sql = SqlQueries.calendar_table_delete 
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    redshift_conn_id = 'redshift',
    dim_sql = SqlQueries.time_table_insert    
    # if you want to delete the table first, please uncomment this one 
    # delete_sql = SqlQueries.time_table_delete 
)

load_reviewer_dimension_table = LoadDimensionOperator(
    task_id='Load_reviewer_dim_table',
    dag=dag,
    redshift_conn_id = 'redshift',
    dim_sql = SqlQueries.reviewer_table_insert    
    # if you want to delete the table first, please uncomment this one 
    # delete_sql = SqlQueries.reviewer_table_delete 
)

load_listing_dimension_table = LoadDimensionOperator(
    task_id='Load_listing_dim_table',
    dag=dag,
    redshift_conn_id = 'redshift',
    dim_sql = SqlQueries.listing_table_insert    
    # if you want to delete the table first, please uncomment this one 
    # delete_sql = SqlQueries.listing_table_delete 
)


run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id = 'redshift',
    table = ['listing','time','reviewer','review','calendar'],
    provide_context = True   
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator.set_downstream([stage_reviews_to_redshift, stage_listings_to_redshift, stage_calendar_to_redshift])
stage_reviews_to_redshift.set_downstream([load_review_table, load_calendar_table])
stage_listings_to_redshift.set_downstream([load_review_table, load_calendar_table])
stage_calendar_to_redshift.set_downstream([load_review_table, load_calendar_table])
load_review_table.set_downstream([load_time_dimension_table,load_reviewer_dimension_table,load_listing_dimension_table])
load_calendar_table.set_downstream([load_time_dimension_table,load_reviewer_dimension_table,load_listing_dimension_table])
run_quality_checks.set_upstream([load_time_dimension_table,load_reviewer_dimension_table,load_listing_dimension_table])
run_quality_checks >> end_operator
