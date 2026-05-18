from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from datetime import datetime, timedelta
import time
import random

df = pd.read_csv('food_delivery_data.csv')
df['order_time'] = pd.to_datetime(df['order_time'])
unique_cities_dates = df[['restaurant_city', 'order_time']].drop_duplicates()
weather_conditions = ['Sunny', 'Rainy', 'Cloudy']
# create a new csv file with city, date and weather condition
weather_data = []
for index, row in unique_cities_dates.iterrows():
    city = row['restaurant_city']
    date = row['order_time'].date()
    weather_condition = random.choice(weather_conditions)
    weather_data.append([city, date, weather_condition])
weather_df = pd.DataFrame(weather_data, columns=['city', 'date', 'weather_condition'])
weather_df.to_csv('weather_data.csv', index=False)
print("Weather data enrichment completed. File saved as 'weather_data.csv'.")


