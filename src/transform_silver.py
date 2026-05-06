import pandas as pd
import os

print("🛠️ [SYSTEM]: Starting transformation of silver data...")

os.makedirs('data/silver', exist_ok=True)

try:
    # 1. Load the raw dataframes
    # NOTE: Code data/raw/ dhoondh raha hai. Make sure folders correct hain!
    raw_df = pd.read_csv('data/raw/food_delivery_data.csv')
    weather_df = pd.read_csv('data/raw/weather_data.csv')
    print("✅ [LOAD]: Raw data loaded successfully.")

    # 2. Robust Date Formatting
    # Hum time ko datetime banake usme se string date nikal rahe hain taaki merge solid ho
    raw_df['order_time'] = pd.to_datetime(raw_df['order_time'])
    raw_df['date'] = raw_df['order_time'].dt.strftime('%Y-%m-%d')
    
    # Weather ki date ko bhi same string format mein laa rahe hain
    weather_df['date'] = pd.to_datetime(weather_df['date']).dt.strftime('%Y-%m-%d')

    print("🔗 [PIPELINE]: Executing join on city and date...")
    
    # 3. The Enterprise Merge
    merged_df = pd.merge(
        raw_df, 
        weather_df, 
        left_on=['restaurant_city', 'date'], 
        right_on=['city', 'date'], 
        how='left'
    )
    
    # Drop redundant 'city' column 
    merged_df.drop(columns=['city'], inplace=True)

    print("⚙️ [PIPELINE]: Feature Engineering...")
    
    # 4. Calculate delivery duration
    merged_df['delivery_time'] = pd.to_datetime(merged_df['delivery_time'])
    merged_df['delivery_duration'] = (merged_df['delivery_time'] - merged_df['order_time']).dt.total_seconds() / 60
    
    # Drop the temporary date column (FinOps optimization)
    merged_df.drop(columns=['date'], inplace=True)

    # 5. Save to highly optimized Parquet format
    merged_df.to_parquet('data/silver/enriched_orders.parquet', index=False)
    print("💾 [SUCCESS]: Transformation completed. Silver data saved as 'enriched_orders.parquet'.")

except Exception as e:
    print(f"❌ [CRITICAL ERROR]: An error occurred during Silver transformation: {e}")