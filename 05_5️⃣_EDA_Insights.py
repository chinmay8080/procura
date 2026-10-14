import streamlit as st
from data_utils import load_data
import pandas as pd
import plotly.express as px

df = load_data()

st.title("📊 Supply Chain Insights & EDA")

# --- 1. Top Selling SKUs by Revenue ---
st.subheader("💰 Top 10 SKUs by Total Revenue")
top_skus = df.groupby("SKU")["Revenue (€)"].sum().sort_values(ascending=False).head(10).reset_index()
fig1 = px.bar(top_skus, x="SKU", y="Revenue (€)", title="Top SKUs by Revenue")
st.plotly_chart(fig1)

# --- 2. Revenue Trend Over Time ---
st.subheader("📈 Revenue Trend Over Time")
df["Date"] = pd.to_datetime(df["Date"])
revenue_trend = df.groupby("Date")["Revenue (€)"].sum().reset_index()
fig2 = px.line(revenue_trend, x="Date", y="Revenue (€)", title="Revenue Trend (All SKUs)")
st.plotly_chart(fig2)

# --- 3. Supplier Performance ---
st.subheader("🏭 Supplier Performance (Total Revenue)")
supplier_perf = df.groupby("Supplier")["Revenue (€)"].sum().sort_values(ascending=False).reset_index()
fig3 = px.bar(supplier_perf, x="Supplier", y="Revenue (€)", title="Revenue by Supplier")
st.plotly_chart(fig3)

# --- 4. Product Category Breakdown ---
st.subheader("📦 Revenue Distribution by Product Category")
category_breakdown = df.groupby("Category")["Revenue (€)"].sum().reset_index()
fig4 = px.pie(category_breakdown, names="Category", values="Revenue (€)", title="Revenue Share by Category")
st.plotly_chart(fig4)

st.success("✅ EDA complete! Use these insights to explain SKU importance, supplier dependency, and sales trends.")
