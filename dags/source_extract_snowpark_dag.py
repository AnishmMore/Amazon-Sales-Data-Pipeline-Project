import os
from snowflake.snowpark import Session
import sys
import logging
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow import DAG

# initiate logging at info level
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%I:%M:%S')

# snowpark session
def get_snowpark_session() -> Session:
    connection_parameters = {
       "account": "account",
        "user": "user",
        "password": "password",
        "ROLE": "SYSADMIN",
        "DATABASE": "sales_dwh",
        "SCHEMA": "source",
        "WAREHOUSE": "SNOWPARK_ETL_WH"
    }
    # creating snowflake session object
    return Session.builder.configs(connection_parameters).create()


def traverse_directory(directory, file_extension):
    file_data = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(file_extension):
                file_path = os.path.join(root, file)
                file_data.append({
                    'name': file,
                    'partition_dir': root.replace(directory, "").strip(os.sep),
                    'local_file_path': file_path
                })
    return file_data

def upload_files(file_data, stage_location):
    session = get_snowpark_session()
    for file_info in file_data:
        session.file.put(
            file_info['local_file_path'], 
            f"{stage_location}/{file_info['partition_dir']}",
            auto_compress=False, overwrite=True, parallel=10
        )

def upload_to_snowflake():
    directory_path = '/Users/anishmore/airflow/sources/sales/'
    stage_location = '@sales_dwh.source.my_internal_stage'

    for file_extension in ['.csv', '.parquet', '.json']:
        file_data = traverse_directory(directory_path, file_extension)
        upload_files(file_data, stage_location)
    
# Define the Airflow DAG
with DAG('source_extract_snowpark_dag',
         schedule_interval=None,
         start_date=datetime(2023, 11, 5),
         catchup=False) as dag:
    
    # Task to clone the repository
    clone_repo_task = BashOperator(
            task_id='clone_repo_task',
            bash_command=f'git clone https://gitlab.com/toppertips/snowflake-work.git /Users/anishmore/airflow/data/'
        )
    # Task to unzip the sales data
    unzip_sales_data_task = BashOperator(
    task_id='unzip_sales_data_task',
    bash_command='unzip /Users/anishmore/airflow/data/snowpark-example/end2end-sample-data/3-region-sales-data.zip -d /Users/anishmore/airflow/sources/'
        )
    # Task to copy the exchange rate data
    copy_exchange_rate_data_task = BashOperator(
    task_id='copy_exchange_rate_data_task',
    bash_command='cp /Users/anishmore/airflow/data/snowpark-example/end2end-sample-data/exchange-rate-data.csv /Users/anishmore/airflow/sources'
        )
    
    # Task to cleanup the cloned repository
    cleanup_repo_task = BashOperator(
        task_id='cleanup_repo_task',
        bash_command=f'rm -rf /Users/anishmore/airflow/data/'
        )
    
    # Task to upload files to Snowflake using Snowpark
    upload_to_snowflake_task = PythonOperator(
        task_id='upload_to_snowflake_task',
        python_callable=upload_to_snowflake,
        dag=dag
    )

    # Define the task sequence in the DAG
    clone_repo_task >> unzip_sales_data_task >> copy_exchange_rate_data_task >> cleanup_repo_task >> upload_to_snowflake_task

    