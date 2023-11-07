import sys
import logging
import pandas as pd

from snowflake.snowpark import Session, DataFrame, CaseExpr
from snowflake.snowpark.functions import col,lit,row_number, rank, split,cast, when, expr,min, max
from snowflake.snowpark.types import StructType, StringType, StructField, StringType,LongType,DecimalType,DateType,TimestampType
from snowflake.snowpark import Window

# initiate logging at info level
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%I:%M:%S')
# Ensure session is correctly established


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

def create_region_dim(all_sales_df,session)-> None:
    region_dim_df = all_sales_df.groupBy(col("Country"),col("Region")).count()
    region_dim_df.show(2)
    region_dim_df = region_dim_df.with_column("isActive",lit('Y'))
    region_dim_df = region_dim_df.selectExpr("sales_dwh.consumption.region_dim_seq.nextval as region_id_pk","Country", "Region", "isActive") 
    #region_dim_df.write.save_as_table('sales_dwh.consumption.region_dim',mode="append")   

    region_dim_df.show(5)
    # part 2 where delta data will be processed 
    
    existing_region_dim_df = session.sql("select Country, Region from sales_dwh.consumption.region_dim")

    region_dim_df = region_dim_df.join(existing_region_dim_df,region_dim_df['Country']==existing_region_dim_df['Country'],join_type='leftanti')
    region_dim_df.show(5)
    intsert_cnt = int(region_dim_df.count())
    if intsert_cnt>0:
        region_dim_df.write.save_as_table("sales_dwh.consumption.region_dim",mode="append")
        print("save operation ran...")
    else:
        print("No insert ...Opps...")


    # have exclude key


def create_product_dim(all_sales_df,session)-> None:

    product_dim_df = all_sales_df.with_column("Brand",split(col('MOBILE_KEY'),lit('/'))[0])     \
                                .with_column("Model",split(col('MOBILE_KEY'),lit('/'))[1])      \
                                .with_column("Color",split(col('MOBILE_KEY'),lit('/'))[2])      \
                                .with_column("Memory",split(col('MOBILE_KEY'),lit('/'))[3])     \
                                .select(col('mobile_key'),col('Brand'),col('Model'),col('Color'),col('Memory'))
    
    product_dim_df = product_dim_df.select(col('mobile_key'),                    \
                                        cast(col('Brand'), StringType()).as_("Brand"),\
                                        cast(col('Model'), StringType()).as_("Model"),\
                                        cast(col('Color'), StringType()).as_("Color"),\
                                        cast(col('Memory'), StringType()).as_("Memory")\
                                        )
    
    product_dim_df = product_dim_df.groupBy(col('mobile_key'),col("Brand"),col("Model"),col("Color"),col("Memory")).count()
    product_dim_df = product_dim_df.with_column("isActive",lit('Y'))

    #fetch existing product dim records.
    existing_product_dim_df = session.sql("select mobile_key, Brand, Model, Color, Memory from sales_dwh.consumption.product_dim")
    existing_product_dim_df.count()

    product_dim_df = product_dim_df.join(existing_product_dim_df,["mobile_key", "Brand", "Model", "Color", "Memory"],join_type='leftanti')

    product_dim_df.show(5)

    product_dim_df = product_dim_df.selectExpr("sales_dwh.consumption.product_dim_seq.nextval as product_id_pk","mobile_key","Brand", "Model","Color","Memory", "isActive") 

    product_dim_df.show(5)
    intsert_cnt = int(product_dim_df.count())
    if intsert_cnt>0:
        product_dim_df.write.save_as_table("sales_dwh.consumption.product_dim",mode="append")
        print("save operation ran...")
    else:
        print("No insert ...Opps...")

def create_promocode_dim(all_sales_df,session)-> None:


    promo_code_dim_df = all_sales_df.with_column( "promotion_code", expr("case when promotion_code is null then 'NA' else promotion_code end"))
    promo_code_dim_df = promo_code_dim_df.groupBy(col("promotion_code"),col("country"),col("region")).count()
    promo_code_dim_df = promo_code_dim_df.with_column("isActive",lit('Y'))

    #promo_code_dim_df.show(10)

    
    #fetch existing product dim records.
    existing_promo_code_dim_df = session.sql("select promotion_code, country, region from sales_dwh.consumption.promo_code_dim")


    promo_code_dim_df = promo_code_dim_df.join(existing_promo_code_dim_df,["promotion_code", "country", "region"],join_type='leftanti')


    promo_code_dim_df = promo_code_dim_df.selectExpr("sales_dwh.consumption.promo_code_dim_seq.nextval as promo_code_id_pk","promotion_code", "country","region","isActive") 


    intsert_cnt = int(promo_code_dim_df.count())
    if intsert_cnt>0:
        promo_code_dim_df.write.save_as_table("sales_dwh.consumption.promo_code_dim",mode="append")
        print("save operation ran...")
    else:
        print("No insert ...Opps...")
    
def create_customer_dim(all_sales_df, session) -> None:
    customer_dim_df = all_sales_df.groupBy(col("COUNTRY"),col("REGION"),col("CUSTOMER_NAME"),col("CONCTACT_NO"),col("SHIPPING_ADDRESS")).count()
    customer_dim_df = customer_dim_df.with_column("isActive",lit('Y'))
    customer_dim_df = customer_dim_df.selectExpr("customer_name", "conctact_no","shipping_address","country","region" ,"isactive") 
    #region_dim_df.write.save_as_table('sales_dwh.consumption.region_dim',mode="append")   

    customer_dim_df.show(5)
    # part 2 where delta data will be processed 
    
    existing_customer_dim_df = session.sql("select customer_name,conctact_no,shipping_address,country, region from sales_dwh.consumption.customer_dim")

    customer_dim_df = customer_dim_df.join(existing_customer_dim_df,["customer_name","conctact_no","shipping_address","country", "region"],join_type='leftanti')

    customer_dim_df = customer_dim_df.selectExpr("sales_dwh.consumption.customer_dim_seq.nextval as customer_id_pk","customer_name", "conctact_no","shipping_address","country","region", "isActive") 

    customer_dim_df.show(5)

    intsert_cnt = int(customer_dim_df.count())
    if intsert_cnt>0:
        customer_dim_df.write.save_as_table("sales_dwh.consumption.customer_dim",mode="append")
        print("save operation ran...")
    else:
        print("No insert ...Opps...")
    
def create_payment_dim(all_sales_df, session) -> None:
    payment_dim_df = all_sales_df.groupBy(col("COUNTRY"),col("REGION"),col("payment_method"),col("payment_provider")).count()
    payment_dim_df = payment_dim_df.with_column("isActive",lit('Y'))

    #region_dim_df.write.save_as_table('sales_dwh.consumption.region_dim',mode="append")   

    payment_dim_df.show(5)
    # part 2 where delta data will be processed 
    
    existing_payment_dim_df = session.sql("select payment_method,payment_provider,country, region from sales_dwh.consumption.payment_dim")

    payment_dim_df = payment_dim_df.join(existing_payment_dim_df,["payment_method","payment_provider","country", "region"],join_type='leftanti')

    payment_dim_df = payment_dim_df.selectExpr("sales_dwh.consumption.payment_dim_seq.nextval as payment_id_pk","payment_method", "payment_provider","country","region", "isActive") 


    intsert_cnt = int(payment_dim_df.count())
    if intsert_cnt>0:
        payment_dim_df.write.save_as_table("sales_dwh.consumption.payment_dim",mode="append")
        print("save operation ran...")
    else:
        print("No insert ...Opps...")

def create_date_dim(all_sales_df, session) -> None:
    start_date = all_sales_df.select(min("order_dt").alias("min_order_dt")).collect()[0].as_dict()['MIN_ORDER_DT']
    end_date = all_sales_df.select(max("order_dt").alias("max_order_dt")).collect()[0].as_dict()['MAX_ORDER_DT']
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    #print(date_range)
    date_dim = pd.DataFrame()
    date_dim['order_dt'] = date_range.date
    date_dim['Year'] = date_range.year
    # Calculate day counter
    start_day_of_year = pd.to_datetime(start_date).dayofyear
    date_dim['DayCounter'] = date_range.dayofyear - start_day_of_year + 1

    date_dim['Month'] = date_range.month
    date_dim['Quarter'] = date_range.quarter
    date_dim['Day'] = date_range.day
    date_dim['DayOfWeek'] = date_range.dayofweek
    date_dim['DayName'] = date_range.strftime('%A')
    date_dim['DayOfMonth'] = date_range.day
    date_dim['Weekday'] = date_dim['DayOfWeek'].map({0: 'Weekday', 1: 'Weekday', 2: 'Weekday', 3: 'Weekday', 4: 'Weekday', 5: 'Weekend', 6: 'Weekend'})


    date_dim_df = session.create_dataframe(date_dim)

    existing_date_dim_df = session.sql("select order_dt from sales_dwh.consumption.date_dim ") 
    date_dim_df = date_dim_df.join(existing_date_dim_df,existing_date_dim_df['order_dt']==date_dim_df['"order_dt"'],join_type='leftanti')

    date_dim_df = date_dim_df.selectExpr(' \
                                   sales_dwh.consumption.date_dim_seq.nextval, \
                                   "order_dt" as order_dt, \
                                   "DayCounter" as day_counter,\
                                   "Year" as order_year, \
                                   "Month" as order_month, \
                                   "Quarter" as order_quarter, \
                                   "Day" as order_day, \
                                   "DayOfWeek" as order_dayofweek, \
                                   "DayName" as order_dayname, \
                                   "DayOfMonth" as order_dayofmonth, \
                                   "Weekday" as order_weekday\
                                   ')

    intsert_cnt = int(date_dim_df.count())
    if intsert_cnt>0:
        date_dim_df.write.save_as_table("sales_dwh.consumption.date_dim",mode="append")
        print("save operation ran...")
    else:
        print("No insert ...Opps...")

def main():
    #get the session object and get dataframe
    session = get_snowpark_session()

    in_sales_df = session.sql("select * from sales_dwh.curated.in_sales_order")
    us_sales_df = session.sql("select * from sales_dwh.curated.us_sales_order")
    fr_sales_df = session.sql("select * from sales_dwh.curated.fr_sales_order")

    all_sales_df = in_sales_df.union(us_sales_df).union(fr_sales_df)

    create_region_dim(all_sales_df,session)     #region dimension
    create_product_dim(all_sales_df,session)    #product dimension
    create_promocode_dim(all_sales_df,session)  #promot code dimension
    create_customer_dim(all_sales_df,session)   #customer dimension
    create_payment_dim(all_sales_df,session)    #payment dimension
    create_date_dim(all_sales_df,session)       #date dimension


    date_dim_df = session.sql("select date_id_pk, order_dt from sales_dwh.consumption.date_dim")
    customer_dim_df = session.sql("select customer_id_pk, customer_name, country, region from sales_dwh.consumption.CUSTOMER_DIM")
    payment_dim_df = session.sql("select payment_id_pk, payment_method, payment_provider, country, region from sales_dwh.consumption.PAYMENT_DIM")
    product_dim_df = session.sql("select product_id_pk, mobile_key from sales_dwh.consumption.PRODUCT_DIM")
    promo_code_dim_df = session.sql("select promo_code_id_pk,promotion_code,country, region from sales_dwh.consumption.PROMO_CODE_DIM")
    region_dim_df = session.sql("select region_id_pk,country, region from sales_dwh.consumption.REGION_DIM")

    all_sales_df = all_sales_df.with_column( "promotion_code", expr("case when promotion_code is null then 'NA' else promotion_code end"))
    all_sales_df = all_sales_df.join(date_dim_df, ["order_dt"],join_type='inner')
    all_sales_df = all_sales_df.join(customer_dim_df, ["customer_name","region","country"],join_type='inner')
    all_sales_df = all_sales_df.join(payment_dim_df, ["payment_method", "payment_provider", "country", "region"],join_type='inner')
    #all_sales_df = all_sales_df.join(product_dim_df, ["brand","model","color","Memory"],join_type='inner')
    all_sales_df = all_sales_df.join(product_dim_df, ["mobile_key"],join_type='inner')
    all_sales_df = all_sales_df.join(promo_code_dim_df, ["promotion_code","country", "region"],join_type='inner')
    all_sales_df = all_sales_df.join(region_dim_df, ["country", "region"],join_type='inner')
    all_sales_df = all_sales_df.selectExpr("sales_dwh.consumption.sales_fact_seq.nextval as order_id_pk, \
                                           order_id as order_code,                               \
                                           date_id_pk as date_id_fk,          \
                                           region_id_pk as region_id_fk,            \
                                           customer_id_pk as customer_id_fk,        \
                                           payment_id_pk as payment_id_fk,          \
                                           product_id_pk as product_id_fk,          \
                                           promo_code_id_pk as promo_code_id_fk,    \
                                           order_quantity,                          \
                                           local_total_order_amt,                   \
                                           local_tax_amt,                           \
                                           exhchange_rate,                          \
                                           us_total_order_amt,                      \
                                           usd_tax_amt                              \
                                           ")
    all_sales_df.write.save_as_table("sales_dwh.consumption.sales_fact",mode="append")


if __name__ == '__main__':
    main()