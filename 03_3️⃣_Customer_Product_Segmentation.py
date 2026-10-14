import streamlit as st
from data_utils import load_data
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Set Streamlit page config
st.set_page_config(page_title="Customer and Product Segmentation" , page_icon="📊",layout="wide")

# Load dataset
df = load_data()

# Get the date range
start_date = df["Date"].min().strftime("%d-%m-%Y")
end_date = df["Date"].max().strftime("%d-%m-%Y")

# Sidebar for navigation
st.sidebar.header("Visualisations")
options = [
    "Sales by Supplier",
    "Sales by Product Family",
    "Sales by Category",
    "Top & Bottom Customers by Revenue",
    "Top & Bottom SKUs by Sales Quantity",
    "Stock Turnover Ratio (Top & Bottom SKUs)"
]
selected_option = st.sidebar.selectbox("Select a Visualisation:", options)

# Function to display Sales by Supplier
def sales_by_supplier():
    supplier_sales = df.groupby("Supplier")["Sales Quantity"].sum().sort_values(ascending=False)
    fig = px.bar(
        supplier_sales,
        x=supplier_sales.index,
        y=supplier_sales.values,
        labels={"x": "Supplier", "y": "Total Sales Quantity"},
        title=f"Total Sales Quantity by Supplier ({start_date} to {end_date})",
        template="plotly_white",
    )
    fig.update_layout(xaxis_tickangle=45, yaxis_tickformat=",")
    st.plotly_chart(fig)

# Function to display Sales by Product Family
def sales_by_product_family():
    product_family_sales = df.groupby("Product_Family_Name")["Sales Quantity"].sum().sort_values(ascending=False)
    fig = px.bar(
        product_family_sales,
        x=product_family_sales.index,
        y=product_family_sales.values,
        labels={"x": "Product Family", "y": "Total Sales Quantity"},
        title=f"Total Sales Quantity by Product Family ({start_date} to {end_date})",
        template="plotly_white",
    )
    fig.update_layout(xaxis_tickangle=45, yaxis_tickformat=",")
    st.plotly_chart(fig)

# Function to display Sales by Category
def sales_by_category():
    category_sales = df.groupby("Category")["Sales Quantity"].sum().sort_values(ascending=False)
    fig = px.bar(
        category_sales,
        x=category_sales.index,
        y=category_sales.values,
        labels={"x": "Category", "y": "Total Sales Quantity"},
        title=f"Total Sales Quantity by Category ({start_date} to {end_date})",
        template="plotly_white",
    )
    fig.update_layout(xaxis_tickangle=45, yaxis_tickformat=",")
    st.plotly_chart(fig)

# Function to display Top & Bottom Customers by Revenue
def customers_by_revenue():
    customer_revenue = df.groupby("Customer ID")["Revenue (€)"].sum().sort_values(ascending=False)
    top_15_customers = customer_revenue.head(15)
    bottom_15_customers = customer_revenue.tail(15)

    # Top 15 Customers
    fig_top = px.bar(
        top_15_customers,
        x=top_15_customers.index,
        y=top_15_customers.values,
        labels={"x": "Customer ID", "y": "Total Revenue (€)"},
        title=f"Top 15 Customers by Revenue (€) ({start_date} to {end_date})",
        template="plotly_white",
    )
    fig_top.update_layout(xaxis_tickangle=90, yaxis_tickformat=",")

    # Bottom 15 Customers
    fig_bottom = px.bar(
        bottom_15_customers,
        x=bottom_15_customers.index,
        y=bottom_15_customers.values,
        labels={"x": "Customer ID", "y": "Total Revenue (€)"},
        title=f"Bottom 15 Customers by Revenue (€) ({start_date} to {end_date})",
        template="plotly_white",
    )
    fig_bottom.update_layout(xaxis_tickangle=90, yaxis_tickformat=",")

    st.plotly_chart(fig_top)
    st.plotly_chart(fig_bottom)

# Function to display Top & Bottom SKUs by Sales Quantity
def skus_by_sales_quantity():
    sku_sales = df.groupby("SKU")["Sales Quantity"].sum().sort_values(ascending=False)
    top_20_skus = sku_sales.head(20)
    bottom_20_skus = sku_sales.tail(20)

    # Top 20 SKUs
    fig_top = px.bar(
        top_20_skus,
        x=top_20_skus.index,
        y=top_20_skus.values,
        labels={"x": "Product SKU", "y": "Total Sales Quantity"},
        title=f"Top 20 Best-Selling SKUs ({start_date} to {end_date})",
        template="plotly_white",
    )
    fig_top.update_layout(xaxis_tickangle=90, yaxis_tickformat=",")

    # Bottom 20 SKUs
    fig_bottom = px.bar(
        bottom_20_skus,
        x=bottom_20_skus.index,
        y=bottom_20_skus.values,
        labels={"x": "Product SKU", "y": "Total Sales Quantity"},
        title=f"Bottom 20 Least-Selling SKUs ({start_date} to {end_date})",
        template="plotly_white",
    )
    fig_bottom.update_layout(xaxis_tickangle=90, yaxis_tickformat=",")

    st.plotly_chart(fig_top)
    st.plotly_chart(fig_bottom)

# Function to display Stock Turnover Ratio
def stock_turnover_ratio():
    stock_turnover = df.groupby("SKU").agg({
        "Sales Quantity": "sum",
        "Stock Level": "mean"
    })

    # Avoid division by zero
    stock_turnover["Stock Level"] = stock_turnover["Stock Level"].replace(0, float("nan")).fillna(1)
    stock_turnover["Stock Turnover Ratio"] = stock_turnover["Sales Quantity"] / stock_turnover["Stock Level"]
    stock_turnover = stock_turnover.replace([float("inf"), -float("inf")], float("nan")).dropna()

    # Top 20 SKUs
    top_20_stock_turnover = stock_turnover.sort_values("Stock Turnover Ratio", ascending=False).head(20)
    fig_top = px.bar(
        top_20_stock_turnover,
        x=top_20_stock_turnover.index,
        y=top_20_stock_turnover["Stock Turnover Ratio"],
        labels={"x": "Product SKU", "y": "Stock Turnover Ratio"},
        title=f"Top 20 SKUs by Stock Turnover Ratio ({start_date} to {end_date})",
        template="plotly_white",
    )
    fig_top.update_layout(xaxis_tickangle=90, yaxis_tickformat=",")

    # Bottom 20 SKUs
    bottom_20_stock_turnover = stock_turnover.sort_values("Stock Turnover Ratio", ascending=False).tail(20)
    fig_bottom = px.bar(
        bottom_20_stock_turnover,
        x=bottom_20_stock_turnover.index,
        y=bottom_20_stock_turnover["Stock Turnover Ratio"],
        labels={"x": "Product SKU", "y": "Stock Turnover Ratio"},
        title=f"Bottom 20 SKUs by Stock Turnover Ratio ({start_date} to {end_date})",
        template="plotly_white",
    )
    fig_bottom.update_layout(xaxis_tickangle=90, yaxis_tickformat=",")

    st.plotly_chart(fig_top)
    st.plotly_chart(fig_bottom)

# Display selected visualisation
if selected_option == "Sales by Supplier":
    sales_by_supplier()
elif selected_option == "Sales by Product Family":
    sales_by_product_family()
elif selected_option == "Sales by Category":
    sales_by_category()
elif selected_option == "Top & Bottom Customers by Revenue":
    customers_by_revenue()
elif selected_option == "Top & Bottom SKUs by Sales Quantity":
    skus_by_sales_quantity()
elif selected_option == "Stock Turnover Ratio (Top & Bottom SKUs)":
    stock_turnover_ratio()
