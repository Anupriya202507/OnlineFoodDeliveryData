import pandas as pd
import sqlalchemy as sqlalchemy
from sqlalchemy import create_engine

username='postgres'
password='Dhashwin05'
port=5432
database_name='OnlineFoodDeliveryDB'
host_name='localhost'  

print("✅ Connected to DB successfully")

engine=create_engine(f'postgresql+psycopg2://{username}:{password}@{host_name}:{port}/{database_name}')


def run_query(query):
    return pd.read_sql(query, engine)

#-----------------------------------------------------
#SQL Queries
#-----------------------------------------------

OnlineFood_DataAnalysis = {

"1.Identify top-spending customers":"""
    SELECT
    customer_id,
    ROUND(SUM(final_amount)::numeric, 2) AS total_spent
    FROM onlinefooddeliverydata
    GROUP BY customer_id
    ORDER BY total_spent DESC
    LIMIT 10; 
""",

"2.Analyze age group vs order value":"""
    SELECT age_group,COUNT(*) AS total_orders, ROUND(AVG(order_value)::numeric, 2) AS
    average_order_value,ROUND(SUM(order_value)::numeric, 2) as total_order_value FROM
    onlinefooddeliverydata GROUP BY age_group ORDER BY total_order_value DESC;
""",

"3.Weekend vs weekday order patterns":"""
    SELECT order_day_type ,COUNT(*) AS total_orders, ROUND(AVG(order_value)::numeric, 2) AS
    average_order_value,SUM(order_value) as total_order_value FROM
    onlinefooddeliverydata GROUP BY order_day_type ORDER BY total_order_value DESC;
""",

"4.Monthly revenue trends":"""
    SELECT
    TO_CHAR(order_date,'Mon') AS month,
    ROUND(SUM(final_amount)::numeric, 2) AS revenue
    FROM onlinefooddeliverydata
    GROUP BY month
    ORDER BY MIN(order_date);;
""",

"5.Impact of discounts on profit":"""
    SELECT discount_applied, COUNT(*) AS total_orders, ROUND(AVG(profit_margin)::numeric, 2)
    AS average_profit_margin FROM
    onlinefooddeliverydata GROUP BY discount_applied ORDER BY discount_applied DESC;
""",

"6.High-revenue cities and cuisines":"""
    SELECT city, cuisine_type, COUNT(*) AS total_orders, ROUND(AVG(order_value)::numeric, 2) 
    AS average_order_value FROM
    onlinefooddeliverydata GROUP BY city, cuisine_type ORDER BY total_orders DESC;
""",

"7.Average delivery time by city":"""
    SELECT city,AVG((delivery_time_min || ' minutes')::interval) AS average_delivery_time FROM
    onlinefooddeliverydata GROUP BY city ORDER BY average_delivery_time ASC;
""",

"8.Distance vs delivery delay analysis":"""
    SELECT distance_km, ROUND(AVG(delivery_time_min)::numeric, 2) AS average_delivery_time FROM
    onlinefooddeliverydata GROUP BY distance_km ORDER BY distance_km ASC;
""",

"9.Delivery rating vs delivery time":"""
    SELECT delivery_rating, ROUND(AVG(delivery_time_min)::numeric, 2) AS average_delivery_time FROM
    onlinefooddeliverydata GROUP BY delivery_rating ORDER BY delivery_rating DESC;
""",

"10.Top-rated restaurants":"""
    SELECT restaurant_id, ROUND(AVG(restaurant_rating)::numeric, 2) AS average_rating,
    COUNT(*) AS total_orders FROM
    onlinefooddeliverydata GROUP BY restaurant_id ORDER BY average_rating DESC LIMIT 10;
""",

"11.Cancellation rate by restaurant":"""
    SELECT restaurant_id, COUNT(*) AS total_orders, ROUND(SUM(CASE WHEN order_status ='Cancelled'
    THEN 1 ELSE 0 END)::numeric / COUNT(*) * 100, 2) AS cancellation_rate
    FROM onlinefooddeliverydata GROUP BY restaurant_id ORDER BY cancellation_rate DESC;
""",

"12.Cuisine-wise performance":"""
    SELECT cuisine_type, COUNT(*) AS total_orders, ROUND(AVG(order_value)::numeric, 2) AS
    average_order_value FROM
    onlinefooddeliverydata GROUP BY cuisine_type ORDER BY total_orders DESC;
""",

"13.Peak hour demand analysis":"""
    SELECT EXTRACT(HOUR FROM order_time) AS order_hour, COUNT(*) AS total_orders
    FROM onlinefooddeliverydata GROUP BY EXTRACT(HOUR FROM order_time) ORDER BY total_orders DESC;
""",    

"14.Payment mode preferences":"""
    SELECT payment_mode, COUNT(*) AS total_orders, ROUND(AVG(order_value)::numeric, 2) AS
    average_order_value FROM
    onlinefooddeliverydata GROUP BY payment_mode ORDER BY total_orders DESC;
""",

"15.Cancellation reason analysis":"""
    SELECT cancellation_reason, COUNT(*) AS total_cancellations FROM
    onlinefooddeliverydata WHERE order_status = 'Cancelled' GROUP BY cancellation_reason
    ORDER BY total_cancellations DESC;
""",
}

for title, query in OnlineFood_DataAnalysis.items():

    print("=" * 80)
    print(title)
    print("=" * 80)

    result = run_query(query)

    print(result)

