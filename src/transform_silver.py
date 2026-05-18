from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import os

print("🛠️ [SYSTEM]: Booting up the PySpark V8 Engine...")

os.makedirs('data/silver', exist_ok=True)

try:
    # 1. Start the Spark Session (The actual engine!)
    spark = SparkSession.builder \
        .appName("SilverLayer_Transformation") \
        .getOrCreate()

    # 2. Load the raw dataframes (PySpark API, NOT Pandas)
    print("✅ [LOAD]: Reading raw CSV files directly into distributed nodes...")
    raw_df = spark.read.csv('data/raw/food_delivery_data.csv', header=True, inferSchema=True)
    weather_df = spark.read.csv('data/raw/weather_data.csv', header=True, inferSchema=True)

    # 3. Robust Date Formatting (PySpark style)
    # Extract date to a new column for matching
    raw_df = raw_df.withColumn("join_date", F.to_date(F.col("order_time")))
    weather_df = weather_df.withColumn("join_date", F.to_date(F.col("date")))

    print("🔗 [PIPELINE]: Executing distributed JOIN on city and date...")
    
    # 4. The Enterprise Merge
    merged_df = raw_df.join(
        weather_df, 
        (raw_df["restaurant_city"] == weather_df["city"]) & (raw_df["join_date"] == weather_df["join_date"]), 
        how="left"
    ).drop(weather_df["city"]).drop("join_date") # Dropping redundant columns straight away

    print("⚙️ [PIPELINE]: Feature Engineering (Delivery Duration)...")
    
    # Calculate delivery duration in minutes using PySpark unix_timestamp
    merged_df = merged_df.withColumn(
        "delivery_duration", 
        (F.unix_timestamp("delivery_time") - F.unix_timestamp("order_time")) / 60
    )

    print("💸 [ENGINE]: Applying Dynamic Surge Pricing...")
    
    # 5. Dynamic Surge Pricing using PySpark when/otherwise (The God-Tier replacement for np.where)
    merged_df = merged_df.withColumn(
        "surge_multiplier",
        F.when(F.col("weather_condition") == "Rainy", 1.25)
         .when(F.col("weather_condition") == "Cloudy", 1.05)
         .otherwise(1.00)
    )

    # Calculate final revenue
    merged_df = merged_df.withColumn(
        "final_revenue",
        F.col("order_amount") * F.col("surge_multiplier")
    )

    # 6. Save to highly optimized Parquet format
    print("💾 [SAVE]: Writing to Silver Parquet...")
    # mode("overwrite") taaki purani file ho toh crash na kare, replace kar de
    merged_df.write.mode("overwrite").parquet('data/silver/enriched_orders.parquet')
    
    print("✅ [SUCCESS]: Transformation completed. Distributed Silver data saved!")

except Exception as e:
    print(f"❌ [CRITICAL ERROR]: An error occurred during PySpark Silver transformation: {e}")