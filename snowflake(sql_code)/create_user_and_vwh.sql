-- create a virtual warehouse
create warehouse snowpark_etl_wh
with
warehouse_size = 'medium'
warehouse_type = 'standard'
auto_suspend = 60
auto_resume = true
min_cluster_count = 1
max_cluster_count = 1
scaling_policy = 'standard';

-- create a snowpark user (it can only be created using accountadmin role)
create user snowpark_user
password = 'TestQ12$4'
comment = 'this is a snowpark user'
default_role = sysadmin
default_secondary_roles = ('ALL')
must_change_password = false;

-- grants
grant role sysadmin to user snowpark_user;
grant USAGE on warehouse snowpark_etl_wh to role sysadmin;
