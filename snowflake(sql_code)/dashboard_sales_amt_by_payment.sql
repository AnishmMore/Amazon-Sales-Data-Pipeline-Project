SELECT 
    dd.order_day,
    pd.payment_method,
    ROUND(SUM(sf.us_total_order_amt), 0) AS daily_sales_amount
FROM 
    consumption.sales_fact sf
JOIN 
    consumption.date_dim dd ON sf.date_id_fk = dd.date_id_pk
JOIN
    consumption.payment_dim pd ON sf.payment_id_fk = pd.payment_id_pk
WHERE 
    dd.order_year = 2020
GROUP BY 
    pd.payment_method, order_day
ORDER BY 
    1;
