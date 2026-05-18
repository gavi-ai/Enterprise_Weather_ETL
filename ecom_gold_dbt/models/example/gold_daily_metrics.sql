{{ config(materialized='table') }}

WITH silver_data AS (
    SELECT * FROM read_parquet('../data/silver/enriched_orders.parquet')
)

SELECT 
    restaurant_city,
    weather_condition,
    COUNT(order_id) as total_orders,
    ROUND(AVG(delivery_duration), 2) as avg_delivery_minutes,
    ROUND(SUM(final_revenue), 2) as total_daily_revenue
FROM silver_data
GROUP BY 
    restaurant_city, 
    weather_condition