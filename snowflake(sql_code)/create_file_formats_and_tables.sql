USE SCHEMA common;

-- Create file formats for CSV, JSON, and Parquet
-- Replace the format names with more descriptive ones

-- CSV file format
CREATE OR REPLACE FILE FORMAT my_csv_format
  TYPE = CSV
  FIELD_DELIMITER = ','
  SKIP_HEADER = 1
  NULL_IF = ('null', 'null')
  EMPTY_FIELD_AS_NULL = TRUE
  FIELD_OPTIONALLY_ENCLOSED_BY = '\042'
  COMPRESSION = AUTO;

-- JSON file format
CREATE OR REPLACE FILE FORMAT my_json_format
  TYPE = JSON
  STRIP_OUTER_ARRAY = TRUE
  COMPRESSION = AUTO;

-- Parquet file format
CREATE OR REPLACE FILE FORMAT my_parquet_format
  TYPE = PARQUET
  COMPRESSION = SNAPPY;

show file formats;

-- Add comments to describe the purpose of each file format
COMMENT ON FILE FORMAT my_csv_format IS 'File format for CSV data from India';
COMMENT ON FILE FORMAT my_json_format IS 'File format for JSON data from France';
COMMENT ON FILE FORMAT my_parquet_format IS 'File format for Parquet data from the USA';

show file formats;
desc file format my_csv_format;



use schema source;

-- Internal Stage - Query The CSV Data File Format
select 
    t.$1::text as order_id, 
    t.$2::text as customer_name, 
    t.$3::text as mobile_key,
    t.$4::number as order_quantity, 
    t.$5::number as unit_price, 
    t.$6::number as order_valaue,  
    t.$7::text as promotion_code , 
    t.$8::number(10,2)  as final_order_amount,
    t.$9::number(10,2) as tax_amount,
    t.$10::date as order_dt,
    t.$11::text as payment_status,
    t.$12::text as shipping_status,
    t.$13::text as payment_method,
    t.$14::text as payment_provider,
    t.$15::text as mobile,
    t.$16::text as shipping_address
 from 
   @my_internal_stage/source=IN/format=csv/
   (file_format => 'sales_dwh.common.my_csv_format') t; 

-- Internal Stage - Query The Parquet Data File Format
select 
  $1:"Order ID"::text as orde_id,
  $1:"Customer Name"::text as customer_name,
  $1:"Mobile Model"::text as mobile_key,
  to_number($1:"Quantity") as quantity,
  to_number($1:"Price per Unit") as unit_price,
  to_decimal($1:"Total Price") as total_price,
  $1:"Promotion Code"::text as promotion_code,
  $1:"Order Amount"::number(10,2) as order_amount,
  to_decimal($1:"Tax") as tax,
  $1:"Order Date"::date as order_dt,
  $1:"Payment Status"::text as payment_status,
  $1:"Shipping Status"::text as shipping_status,
  $1:"Payment Method"::text as payment_method,
  $1:"Payment Provider"::text as payment_provider,
  $1:"Phone"::text as phone,
  $1:"Delivery Address"::text as shipping_address
from 
     @sales_dwh.source.my_internal_stage/source=US/format=parquet/
     (file_format => 'sales_dwh.common.my_parquet_format');

-- Internal Stage - Query The JSON Data File Format
select                                                       
    $1:"Order ID"::text as orde_id,                   
    $1:"Customer Name"::text as customer_name,          
    $1:"Mobile Model"::text as mobile_key,              
    to_number($1:"Quantity") as quantity,               
    to_number($1:"Price per Unit") as unit_price,       
    to_decimal($1:"Total Price") as total_price,        
    $1:"Promotion Code"::text as promotion_code,        
    $1:"Order Amount"::number(10,2) as order_amount,    
    to_decimal($1:"Tax") as tax,                        
    $1:"Order Date"::date as order_dt,                  
    $1:"Payment Status"::text as payment_status,        
    $1:"Shipping Status"::text as shipping_status,      
    $1:"Payment Method"::text as payment_method,        
    $1:"Payment Provider"::text as payment_provider,    
    $1:"Phone"::text as phone,                          
    $1:"Delivery Address"::text as shipping_address
from                                                
@sales_dwh.source.my_internal_stage/source=FR/format=json/
(file_format => sales_dwh.common.my_json_format);

use schema common;
create or replace transient table exchange_rate(
    date date, 
    usd2usd decimal(10,7),
    usd2eu decimal(10,7),
    usd2can decimal(10,7),
    usd2uk decimal(10,7),
    usd2inr decimal(10,7),
    usd2jp decimal(10,7)
);

copy into sales_dwh.common.exchange_rate
from 
(
select 
    t.$1::date as exchange_dt,
    to_decimal(t.$2) as usd2usd,
    to_decimal(t.$3,12,10) as usd2eu,
    to_decimal(t.$4,12,10) as usd2can,
    to_decimal(t.$4,12,10) as usd2uk,
    to_decimal(t.$4,12,10) as usd2inr,
    to_decimal(t.$4,12,10) as usd2jp
from 
     @sales_dwh.source.my_internal_stage/exchange/exchange-rate-data.csv
     (file_format => 'sales_dwh.common.my_csv_format') t
);

select * from sales_dwh.common.exchange_rate;


//since did not have data for 2020 exhange rate converted the data from 2023 to 2020, in real case scenario we need to get the need for that from some api, but here i just did this for project purpose

use schema common;

UPDATE sales_dwh.common.exchange_rate
SET date = DATEADD(YEAR, -3, date)
WHERE YEAR(date) = 2023;

select * from sales_dwh.common.exchange_rate;
