import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import random

print("Starting data generation...")

# food delivery transaction accross different cities of india with order_is, customer_id, restaurant_city, order_amount, order_time, delivery_time
cities = ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata']
data = []
for i in range(100000):
    order_id = f"ORD{100000 + i}"
    customer_id = f"CUST{random.randint(1000, 9999)}"
    restaurant_city = random.choice(cities)
    order_amount = round(random.uniform(100, 1000), 2)
    order_time = datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23), minutes=random.randint(0, 59))
    delivery_time = order_time + timedelta(minutes=random.randint(30, 120))
    
    data.append([order_id, customer_id, restaurant_city, order_amount, order_time.strftime('%Y-%m-%d %H:%M:%S'), delivery_time.strftime('%Y-%m-%d %H:%M:%S')])

df = pd.DataFrame(data, columns=['order_id', 'customer_id', 'restaurant_city', 'order_amount', 'order_time', 'delivery_time'])
df.to_csv('food_delivery_data.csv', index=False)
print("Data generation completed. File saved as 'food_delivery_data.csv'.")