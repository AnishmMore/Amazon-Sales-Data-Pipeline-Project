-- region dimension
use schema consumption;
create or replace sequence region_dim_seq start = 1 increment = 1;
create or replace transient table region_dim(
    region_id_pk number primary key,
    Country text, 
    Region text,
    isActive text(1)
);


-- product dimension
create or replace sequence product_dim_seq start = 1 increment = 1;
create or replace transient table product_dim(
    product_id_pk number primary key,
    Mobile_key text,
    Brand text, 
    Model text,
    Color text,
    Memory text,
    isActive text(1)
);

-- promo_code dimension
create or replace sequence promo_code_dim_seq start = 1 increment = 1;
create or replace transient table promo_code_dim(
    promo_code_id_pk number primary key,
    PROMOTION_CODE text,
    country text,
    region text,
    isActive text(1)
);

-- customer dimension
create or replace sequence customer_dim_seq start = 1 increment = 1;
create or replace transient table customer_dim(
    customer_id_pk number primary key,
    customer_name text,
    CONCTACT_NO text,
    SHIPPING_ADDRESS text,
    country text,
    region text,
    isActive text(1)
);

-- payment dimension
create or replace sequence payment_dim_seq start = 1 increment = 1;
create or replace transient table payment_dim(
    payment_id_pk number primary key,
    PAYMENT_METHOD text,
    PAYMENT_PROVIDER text,
    country text,
    region text,
    isActive text(1)
);
-- date dimension
create or replace sequence date_dim_seq start = 1 increment = 1;
create or replace transient table date_dim(
    date_id_pk int primary key,
    order_dt date,
    day_counter int,
    order_year int,
    order_month int,
    order_quater int,
    order_day int,
    order_dayofweek int,
    order_dayname text,
    order_dayofmonth int,
    order_weekday text
);

-- fact tables
create or replace sequence sales_fact_seq start = 1 increment = 1;
create or replace table sales_fact (
 order_id_pk number(38,0),
 order_code varchar(),
 date_id_fk number(38,0),
 region_id_fk number(38,0),
 customer_id_fk number(38,0),
 payment_id_fk number(38,0),
 product_id_fk number(38,0),
 promo_code_id_fk number(38,0),
 order_quantity number(38,0),
 local_total_order_amt number(10,2),
 local_tax_amt number(10,2),
 exhchange_rate number(15,7),
 us_total_order_amt number(23,8),
 usd_tax_amt number(23,8)
);

-- Table Containts
alter table sales_fact add
    constraint fk_sales_region FOREIGN KEY (REGION_ID_FK) REFERENCES region_dim (REGION_ID_PK) NOT ENFORCED;

alter table sales_fact add
    constraint fk_sales_date FOREIGN KEY (DATE_ID_FK) REFERENCES date_dim (DATE_ID_PK) NOT ENFORCED;

alter table sales_fact add
    constraint fk_sales_customer FOREIGN KEY (CUSTOMER_ID_FK) REFERENCES customer_dim (CUSTOMER_ID_PK) NOT ENFORCED;
--
alter table sales_fact add
    constraint fk_sales_payment FOREIGN KEY (PAYMENT_ID_FK) REFERENCES payment_dim (PAYMENT_ID_PK) NOT ENFORCED;

alter table sales_fact add
    constraint fk_sales_product FOREIGN KEY (PRODUCT_ID_FK) REFERENCES product_dim (PRODUCT_ID_PK) NOT ENFORCED;

alter table sales_fact add
    constraint fk_sales_promot FOREIGN KEY (PROMO_CODE_ID_FK) REFERENCES promo_code_dim (PROMO_CODE_ID_PK) NOT ENFORCED;




















