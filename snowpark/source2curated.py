import sys
import logging

from snowflake.snowpark import Session, DataFrame
from snowflake.snowpark.functions import col, lit, rank
from snowflake.snowpark import Window

# initiate logging at info level
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%I:%M:%S')


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


def filter_dataset(df: DataFrame, column_name: str, filter_criterion: str) -> DataFrame:
    return df.filter(col(column_name) == filter_criterion)


def main():
    session = get_snowpark_session()

    # IN region processing
    sales_df_in = session.sql("select * from sales_dwh.source.in_sales_order")
    processed_df_in = process_sales_data(sales_df_in, 'IN', 'APAC', 'INR', 'USD2INR','MOBILE')

    # US region processing
    sales_df_us = session.sql("select * from sales_dwh.source.us_sales_order")
    processed_df_us = process_sales_data(sales_df_us, 'US', 'NA', 'USD', 'USD2USD','PHONE')

    # FR region processing
    sales_df_fr = session.sql("select * from sales_dwh.source.fr_sales_order")
    processed_df_fr = process_sales_data(sales_df_fr, 'FR', 'EU', 'EUR', 'USD2EU','PHONE')

    # Further processing can be done if required...


def process_sales_data(sales_df: DataFrame, country_code: str, region_name: str, local_currency: str, exchange_rate_column: str,contact_column: str) -> DataFrame:
    paid_sales_df = filter_dataset(sales_df, 'PAYMENT_STATUS', 'Paid')
    shipped_sales_df = filter_dataset(paid_sales_df, 'SHIPPING_STATUS', 'Delivered')
    country_sales_df = shipped_sales_df.with_column('Country', lit(country_code)).with_column('Region', lit(region_name))

    forex_df = get_snowpark_session().sql("select * from sales_dwh.common.exchange_rate")
    sales_with_forex_df = country_sales_df.join(forex_df, country_sales_df['order_dt'] == forex_df['date'], join_type='outer')

    unique_orders = sales_with_forex_df.with_column('order_rank', rank().over(
        Window.partitionBy(col("order_dt")).order_by(col('_metadata_last_modified').desc()))).filter(
        col("order_rank") == 1).select(col('SALES_ORDER_KEY').alias('unique_sales_order_key'))

    final_sales_df = unique_orders.join(sales_with_forex_df, unique_orders['unique_sales_order_key'] == sales_with_forex_df['SALES_ORDER_KEY'], join_type='inner')
    # Build final data frame selection here...
    final_sales_df = final_sales_df.select(
        col('SALES_ORDER_KEY'),
        col('ORDER_ID'),
        col('ORDER_DT'),
        col('CUSTOMER_NAME'),
        col('MOBILE_KEY'),
        col('Country'),
        col('Region'),
        col('ORDER_QUANTITY'),
        lit(local_currency).alias('LOCAL_CURRENCY'),
        col('UNIT_PRICE').alias('LOCAL_UNIT_PRICE'),
        col('PROMOTION_CODE'),
        col('FINAL_ORDER_AMOUNT').alias('LOCAL_TOTAL_ORDER_AMT'),
        col('TAX_AMOUNT').alias('local_tax_amt'),
        col(exchange_rate_column).alias("Exchange_Rate"),
        (col('FINAL_ORDER_AMOUNT') / col(exchange_rate_column)).alias('USD_TOTAL_ORDER_AMT'),
        (col('TAX_AMOUNT') / col(exchange_rate_column)).alias('USD_TAX_AMT'),
        col('payment_status'),
        col('shipping_status'),
        col('payment_method'),
        col('payment_provider'),
        col(contact_column).alias('CONTACT_NO'),
        col('shipping_address')
    )

    # Depending on the region, you can customize the save location or additional logic
    final_sales_df.write.save_as_table(f"sales_dwh.curated.{country_code.lower()}_sales_order", mode="append")

    return final_sales_df


if __name__ == '__main__':
    main()
