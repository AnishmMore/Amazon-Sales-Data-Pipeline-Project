import os
from snowflake.snowpark import Session
import sys
import logging

# initiate logging at info level
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%I:%M:%S')

# snowpark session
def get_snowpark_session() -> Session:
    connection_parameters = {
        "account": "account",
        "user": "user",
        "password": "password",
        "role": "SYSADMIN",
        "database": "sales_dwh",
        "schema": "source",
        "warehouse": "SNOWPARK_ETL_WH"
    }
    # creating snowflake session object
    return Session.builder.configs(connection_parameters).create()

def upload_file(local_file_path, stage_location):
    session = get_snowpark_session()
    # logging info about the file to be uploaded
    logging.info(f"Uploading file {local_file_path} to {stage_location}")
    session.file.put(
        local_file_path,
        stage_location,
        auto_compress=False,
        overwrite=True,
        parallel=10
    )
    logging.info(f"Uploaded file {local_file_path} to {stage_location}")

def main():
    local_file_path = '/Users/anishmore/airflow/sources/exchange-rate-data.csv'
    stage_location = '@my_internal_stage/exchange/'

    upload_file(local_file_path, stage_location)

if __name__ == '__main__':
    main()
