from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import os

print("🏆 [SYSTEM]: Booting up the Gold Layer (Business Aggregations)...")

os.makedirs('data/gold', exist_ok=True)

try:
    # 1. Load the Silver Parquet file 
    print("📥 [LOAD]: Reading enriched data from Silver layer...")
    df = pd.read_parquet('data/silver/enriched_orders.parquet')

    print("📊 [PIPELINE]: Crunching weather-based business metrics...")
    
    # 2. The Gold Aggregation
    gold_df = df.groupby(['restaurant_city', 'weather_condition']).agg(
        total_orders=pd.NamedAgg(column='order_id', aggfunc='count'),
        avg_delivery_duration=pd.NamedAgg(column='delivery_duration', aggfunc='mean'),
        # BUG FIXED: Changed 'order_value' to 'order_amount'
        total_revenue=pd.NamedAgg(column='final_revenue', aggfunc='sum')
    ).reset_index()
    
    # 3. Clean up the numbers for the final dashboard presentation
    gold_df['avg_delivery_duration'] = gold_df['avg_delivery_duration'].round(2)
    gold_df['total_revenue'] = gold_df['total_revenue'].round(2)
        
    # 4. Save the gold data
    gold_df.to_parquet('data/gold/gold_metrics.parquet', index=False)
    print("✅ [SUCCESS]: Gold layer transformation complete! Metrics saved as 'gold_metrics.parquet'.")

except Exception as e:
    print(f"❌ [ERROR]: An error occurred during Gold layer transformation: {e}")