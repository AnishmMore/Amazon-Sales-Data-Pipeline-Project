use schema curated;
create or replace sequence in_sales_order_seq 
  start = 1 
  increment = 1 
comment='This is sequence for India sales order table';

create or replace sequence us_sales_order_seq 
  start = 1 
  increment = 1 
  comment='This is sequence for USA sales order table';

create or replace sequence fr_sales_order_seq 
  start = 1 
  increment = 1 
  comment='This is sequence for France sales order table';

grant all on sequence in_sales_order_seq to role SYSADMIN;
grant all on sequence us_sales_order_seq to role SYSADMIN;
grant all on sequence fr_sales_order_seq to role SYSADMIN;


show sequences;


-- curated India sales order table
create or replace table in_sales_order (
 sales_order_key number(38,0),
 order_id varchar(),
 order_dt date,
 customer_name varchar(),
 mobile_key varchar(),
 country varchar(),
 region varchar(),
 order_quantity number(38,0),
 local_currency varchar(),
 local_unit_price number(38,0),
 promotion_code varchar(),
 local_total_order_amt number(10,2),
 local_tax_amt number(10,2),
 exhchange_rate number(15,7),
 us_total_order_amt number(23,8),
 usd_tax_amt number(23,8),
 payment_status varchar(),
 shipping_status varchar(),
 payment_method varchar(),
 payment_provider varchar(),
 conctact_no varchar(),
 shipping_address varchar()
);

-- curated US sales order table
create or replace table us_sales_order (
 sales_order_key number(38,0),
 order_id varchar(),
 order_dt date,
 customer_name varchar(),
 mobile_key varchar(),
 country varchar(),
 region varchar(),
 order_quantity number(38,0),
 local_currency varchar(),
 local_unit_price number(38,0),
 promotion_code varchar(),
 local_total_order_amt number(10,2),
 local_tax_amt number(10,2),
 exhchange_rate number(15,7),
 us_total_order_amt number(23,8),
 usd_tax_amt number(23,8),
 payment_status varchar(),
 shipping_status varchar(),
 payment_method varchar(),
 payment_provider varchar(),
 conctact_no varchar(),
 shipping_address varchar()
);

-- -- curated FR sales order table
create or replace table fr_sales_order (
 sales_order_key number(38,0),
 order_id varchar(),
 order_dt date,
 customer_name varchar(),
 mobile_key varchar(),
 country varchar(),
 region varchar(),
 order_quantity number(38,0),
 local_currency varchar(),
 local_unit_price number(38,0),
 promotion_code varchar(),
 local_total_order_amt number(10,2),
 local_tax_amt number(10,2),
 exhchange_rate number(15,7),
 us_total_order_amt number(23,8),
 usd_tax_amt number(23,8),
 payment_status varchar(),
 shipping_status varchar(),
 payment_method varchar(),
 payment_provider varchar(),
 conctact_no varchar(),
 shipping_address varchar()
);

grant all on table in_sales_order to role SYSADMIN;
grant all on table us_sales_order to role SYSADMIN;
grant all on table fr_sales_order to role SYSADMIN;

select * from sales_dwh.curated.us_sales_order;
