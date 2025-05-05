import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
print("🚀 Dashboard is starting...")


# Database credentials
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")

# Connect to MySQL
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}')
df = pd.read_sql("SELECT * FROM orderData", con=engine)

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Olist Orders Dashboard"

# Example charts
fig1 = px.histogram(df, x="order_status", title="Order Status Distribution")

fig2 = px.box(df, x="product_category_name", y="price", title="Product Price Distribution",
              labels={"product_category_name": "Product Category"}, height=600)
fig2.update_layout(xaxis_tickangle=-45)

fig3 = px.scatter(df, x="order_purchase_timestamp", y="price",
                  color="order_status", title="Price Over Time")

# Layout
app.layout = html.Div([
    html.H1("📦 Olist E-Commerce Dashboard", style={'textAlign': 'center'}),
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3),
])

if __name__ == '__main__':
    app.run(debug=True)
