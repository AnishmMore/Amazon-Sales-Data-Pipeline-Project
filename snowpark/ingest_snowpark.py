import sys
import logging

from snowflake.snowpark import Session, DataFrame
from snowflake.snowpark.types import StructType, StringType, StructField, StringType,LongType,DecimalType,DateType,TimestampType
from snowflake.snowpark.functions import col,lit,row_number, rank
from snowflake.snowpark import Window

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

def ingest_in_sales(session)-> None:
    session.sql(" \
            copy into sales_dwh.source.in_sales_order from ( \
            select \
            in_sales_order_seq.nextval, \
            t.$1::text as order_id, \
            t.$2::text as customer_name, \
            t.$3::text as mobile_key,\
            t.$4::number as order_quantity, \
            t.$5::number as unit_price, \
            t.$6::number as order_valaue,  \
            t.$7::text as promotion_code , \
            t.$8::number(10,2)  as final_order_amount,\
            t.$9::number(10,2) as tax_amount,\
            t.$10::date as order_dt,\
            t.$11::text as payment_status,\
            t.$12::text as shipping_status,\
            t.$13::text as payment_method,\
            t.$14::text as payment_provider,\
            t.$15::text as mobile,\
            t.$16::text as shipping_address,\
            metadata$filename as stg_file_name,\
            metadata$file_row_number as stg_row_numer,\
            metadata$file_last_modified as stg_last_modified\
            from \
            @sales_dwh.source.my_internal_stage/source=IN/format=csv/ \
            (                                                             \
                file_format => 'sales_dwh.common.my_csv_format'           \
            ) t  )  on_error = 'Continue'     \
            "
            ).collect()

def ingest_us_sales(session)-> None:
    session.sql(' \
            copy into sales_dwh.source.us_sales_order                \
            from                                    \
            (                                       \
                select                              \
                us_sales_order_seq.nextval, \
                $1:"Order ID"::text as orde_id,   \
                $1:"Customer Name"::text as customer_name,\
                $1:"Mobile Model"::text as mobile_key,\
                to_number($1:"Quantity") as quantity,\
                to_number($1:"Price per Unit") as unit_price,\
                to_decimal($1:"Total Price") as total_price,\
                $1:"Promotion Code"::text as promotion_code,\
                $1:"Order Amount"::number(10,2) as order_amount,\
                to_decimal($1:"Tax") as tax,\
                $1:"Order Date"::date as order_dt,\
                $1:"Payment Status"::text as payment_status,\
                $1:"Shipping Status"::text as shipping_status,\
                $1:"Payment Method"::text as payment_method,\
                $1:"Payment Provider"::text as payment_provider,\
                $1:"Phone"::text as phone,\
                $1:"Delivery Address"::text as shipping_address,\
                metadata$filename as stg_file_name,\
                metadata$file_row_number as stg_row_numer,\
                metadata$file_last_modified as stg_last_modified\
                from                                \
                    @sales_dwh.source.my_internal_stage/source=US/format=parquet/\
                    (file_format => sales_dwh.common.my_parquet_format)\
                    ) on_error = continue \
            '
            ).collect()
    
def ingest_fr_sales(session)-> None:
    session.sql(' \
        copy into sales_dwh.source.fr_sales_order                                \
        from                                                    \
        (                                                       \
            select                                              \
            sales_dwh.source.fr_sales_order_seq.nextval,         \
            $1:"Order ID"::text as orde_id,                   \
            $1:"Customer Name"::text as customer_name,          \
            $1:"Mobile Model"::text as mobile_key,              \
            to_number($1:"Quantity") as quantity,               \
            to_number($1:"Price per Unit") as unit_price,       \
            to_decimal($1:"Total Price") as total_price,        \
            $1:"Promotion Code"::text as promotion_code,        \
            $1:"Order Amount"::number(10,2) as order_amount,    \
            to_decimal($1:"Tax") as tax,                        \
            $1:"Order Date"::date as order_dt,                  \
            $1:"Payment Status"::text as payment_status,        \
            $1:"Shipping Status"::text as shipping_status,      \
            $1:"Payment Method"::text as payment_method,        \
            $1:"Payment Provider"::text as payment_provider,    \
            $1:"Phone"::text as phone,                          \
            $1:"Delivery Address"::text as shipping_address ,    \
            metadata$filename as stg_file_name,\
            metadata$file_row_number as stg_row_numer,\
            metadata$file_last_modified as stg_last_modified\
            from                                                \
            @sales_dwh.source.my_internal_stage/source=FR/format=json/\
            (file_format => sales_dwh.common.my_json_format)\
            ) on_error=continue\
        '
        ).collect()

def main():

    #get the session object and get dataframe
    session = get_snowpark_session()
    
    ingest_in_sales(session)
    ingest_us_sales(session)     
    ingest_fr_sales(session)   

if __name__ == '__main__':
    main()