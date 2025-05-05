import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load the dataset
orders = pd.read_csv("csv/olist_orders_dataset.csv", encoding="latin1")
items = pd.read_csv("csv/olist_order_items_dataset.csv", encoding="latin1")
products = pd.read_csv("csv/olist_products_dataset.csv", encoding="latin1")
customers = pd.read_csv("csv/olist_customers_dataset.csv", encoding="latin1")
reviews = pd.read_csv("csv/olist_order_reviews_dataset.csv", encoding="latin1")

def transform():
    customersData = pd.read_csv("csv/olist_customers_dataset.csv", encoding="latin1")
    customersData =customersData.drop(columns=['customer_unique_id'])
    # --------------------------------------------------------------------
    ordersData = pd.read_csv("csv/olist_orders_dataset.csv", encoding="latin1")
    ordersData['order_approved_at'] = ordersData['order_approved_at'].fillna('Not Approved')
    ordersData['order_delivered_carrier_date'] = ordersData['order_delivered_carrier_date'].fillna('Not Shipped')
    ordersData['order_delivered_customer_date'] = ordersData['order_delivered_customer_date'].fillna('Not Delivered')
    ordersData.dropna(subset=[
        'order_approved_at',
        'order_delivered_carrier_date',
        'order_delivered_customer_date'
    ], inplace=True)
    data =['order_estimated_delivery_date','order_approved_at','order_delivered_carrier_date','order_delivered_customer_date']
    for col in data:
        if col in ordersData.columns:
         ordersData[col] = pd.to_datetime(ordersData[col], errors='coerce')
# -------------------------------------------------------------------------------------------------
    itemsData = pd.read_csv("csv/olist_order_items_dataset.csv", encoding="latin1")
    itemsData['shipping_limit_date'] = pd.to_datetime(itemsData['shipping_limit_date'])
# --------------------------------------------------------------------------------------------
    productsData = pd.read_csv("csv/olist_products_dataset.csv", encoding="latin1")
    productsData.dropna(inplace=True)
    
# --------------------------------------------------------------------------------------------
    reviewsData = pd.read_csv("csv/olist_order_reviews_dataset.csv", encoding="latin1")
    reviewsData['review_creation_date'] = pd.to_datetime(reviewsData['review_creation_date'])
    reviewsData['review_answer_timestamp'] = pd.to_datetime(reviewsData['review_answer_timestamp'])
    # 1. Merge orders with customers
    orders_customers = pd.merge(ordersData, customersData, on='customer_id', how='inner')

# 2. Merge with order items
    orders_customers_items = pd.merge(orders_customers, itemsData, on='order_id', how='inner')

# 3. Merge with products
    full_data = pd.merge(orders_customers_items, productsData, on='product_id', how='inner')

# 4. Merge with reviews
    final_data = pd.merge(full_data, reviewsData, on='order_id', how='left')
    final_data.to_csv('CSVnew/cleanedData.csv' ,index=True)



transform()

def load_to_mysql():
   
    load_dotenv()

    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")

    engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')

    # Read cleaned CSVs
    final_data = pd.read_csv('CSVnew/cleanedData.csv', index_col=0)

    # Load into MySQL
    final_data.to_sql("orderData", con=engine, if_exists="replace", index=False)

    print("✅ All data loaded into MySQL successfully.")

load_to_mysql()
