# 🧹 Olist Data Cleaning & Visualization Dashboard

This project involves cleaning, transforming, and visualizing real-world e-commerce data from the Olist dataset. The goal is to build a complete data pipeline that extracts, transforms, loads, and visualizes customer, order, product, and review data.

## 🔧 Tech Stack

- Python
- Pandas
- MySQL
- SQLAlchemy
- Dash (Plotly)
- dotenv (for environment management)

## 📁 Project Structure

├── csv/ # Raw CSV datasets
├── CSVnew/ # Cleaned data
├── dashboard.py # Dash dashboard script
├── etl_script.py # ETL pipeline script
├── .env # Environment variables (DB credentials)
├── README.md # Project documentation


## 🔄 ETL Process

1. **Extract**: Loads raw data from CSV files.
2. **Transform**: Cleans null values, merges datasets, handles dates.
3. **Load**: Saves the cleaned dataset into MySQL using SQLAlchemy.

## 📊 Dashboard Features

- Total Orders & Customers
- Delivery Status Overview
- Review Score Breakdown
- Product Category Insights

## 🚀 How to Run

1. Clone the repository  
2. Install dependencies  
   ```bash
   pip install -r requirements.txt
