list @my_internal_stage;
REMOVE @my_internal_stage pattern='.*';

list @my_internal_stage/source=FR/;
list @my_internal_stage/source=IN/;
list @my_internal_stage/source=US/;

LIST @my_internal_stage/exchange;
