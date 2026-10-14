import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from data_utils import load_data


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Business Analytics",
    page_icon="💼",
    layout="wide"
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = load_data()

df["Date"] = pd.to_datetime(df["Date"])

# Remove unnecessary missing rows
df = df.dropna(subset=["SKU", "Revenue (€)", "Sales Quantity"])


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("💼 Business Analytics & Decision Support")

st.markdown("""
This module converts Procura's analytical results into
business-oriented insights and decisions.
""")


# ---------------------------------------------------------
# DATASET VALIDATION
# ---------------------------------------------------------

st.header("🔎 1. Dataset Validation")

required_columns = [
    "Date",
    "SKU",
    "Sales Quantity",
    "Revenue (€)",
    "Supplier",
    "Category",
    "Product_Family_Name"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Records", f"{len(df):,}")

with col2:
    st.metric("Unique SKUs", f"{df['SKU'].nunique():,}")

with col3:
    st.metric("Missing Values", f"{df.isna().sum().sum():,}")

with col4:
    st.metric("Duplicate Rows", f"{df.duplicated().sum():,}")


if missing_columns:
    st.error(
        f"Missing required columns: {', '.join(missing_columns)}"
    )
else:
    st.success("✅ Dataset contains all required columns.")


# ---------------------------------------------------------
# REVENUE VALIDATION
# ---------------------------------------------------------

st.header("💰 2. Revenue Validation")

st.markdown("""
Revenue should be calculated consistently from the underlying
transaction data. Procura uses the existing **Revenue (€)**
field as the source of truth.
""")

revenue_check = df["Revenue (€)"].describe()

st.dataframe(
    revenue_check.to_frame().round(2),
    use_container_width=True
)

# Check invalid revenue
negative_revenue = (df["Revenue (€)"] < 0).sum()

if negative_revenue == 0:
    st.success("✅ No negative revenue values found.")
else:
    st.warning(
        f"⚠️ {negative_revenue} records contain negative revenue."
    )


# ---------------------------------------------------------
# REVENUE TREND
# ---------------------------------------------------------

st.header("📈 3. Revenue Trend Analysis")

revenue_trend = (
    df.groupby("Date")["Revenue (€)"]
    .sum()
    .reset_index()
)

fig_revenue = px.line(
    revenue_trend,
    x="Date",
    y="Revenue (€)",
    title="Revenue Trend Over Time",
    markers=True
)

fig_revenue.update_layout(
    xaxis_title="Date",
    yaxis_title="Revenue (€)"
)

st.plotly_chart(
    fig_revenue,
    use_container_width=True
)


# ---------------------------------------------------------
# PROFIT ANALYSIS
# ---------------------------------------------------------

st.header("📊 4. Profit Analysis")

st.info("""
Profit analysis requires a cost field. If your dataset contains
a cost column, the application calculates:

Profit = Revenue − Cost

If no cost field exists, profit cannot be calculated reliably
without introducing an assumption.
""")


# Detect possible cost columns
possible_cost_columns = [
    "Cost (€)",
    "Cost",
    "Total Cost",
    "Total Cost (€)",
    "COGS",
    "COGS (€)",
    "Purchase Cost",
    "Purchase Cost (€)"
]

cost_column = None

for col in possible_cost_columns:
    if col in df.columns:
        cost_column = col
        break


if cost_column:

    df["Profit"] = df["Revenue (€)"] - df[cost_column]

    df["Profit Margin (%)"] = np.where(
        df["Revenue (€)"] != 0,
        (df["Profit"] / df["Revenue (€)"]) * 100,
        0
    )

    p1, p2, p3 = st.columns(3)

    with p1:
        st.metric(
            "Total Revenue",
            f"€{df['Revenue (€)'].sum():,.2f}"
        )

    with p2:
        st.metric(
            "Total Cost",
            f"€{df[cost_column].sum():,.2f}"
        )

    with p3:
        st.metric(
            "Total Profit",
            f"€{df['Profit'].sum():,.2f}"
        )

    profit_product = (
        df.groupby("SKU")["Profit"]
        .sum()
        .sort_values(ascending=False)
        .head(20)
        .reset_index()
    )

    fig_profit = px.bar(
        profit_product,
        x="SKU",
        y="Profit",
        title="Top Products by Profit"
    )

    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )

else:

    st.warning(
        "⚠️ No cost column was found in the current dataset. "
        "Profit is therefore not calculated."
    )


# ---------------------------------------------------------
# PRODUCT BASED ANALYSIS
# ---------------------------------------------------------

st.header("📦 5. Product-Based Analysis")

product_analysis = (
    df.groupby("SKU")
    .agg(
        Revenue=("Revenue (€)", "sum"),
        Quantity=("Sales Quantity", "sum")
    )
    .sort_values("Revenue", ascending=False)
    .reset_index()
)

fig_product = px.bar(
    product_analysis.head(20),
    x="SKU",
    y="Revenue",
    title="Top 20 Products by Revenue"
)

st.plotly_chart(
    fig_product,
    use_container_width=True
)

st.dataframe(
    product_analysis.head(20),
    use_container_width=True
)


# ---------------------------------------------------------
# QUANTITY BASED ANALYSIS
# ---------------------------------------------------------

st.header("📦 6. Quantity-Based Analysis")

quantity_analysis = (
    df.groupby("SKU")["Sales Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(20)
    .reset_index()
)

fig_quantity = px.bar(
    quantity_analysis,
    x="SKU",
    y="Sales Quantity",
    title="Top 20 Products by Sales Quantity"
)

st.plotly_chart(
    fig_quantity,
    use_container_width=True
)


# ---------------------------------------------------------
# ABC ANALYSIS
# ---------------------------------------------------------

st.header("🅰️🅱️©️ 7. ABC Analysis")

st.markdown("""
ABC Analysis classifies products according to their contribution
to total revenue.

**A:** High-value products  
**B:** Medium-value products  
**C:** Low-value products
""")


abc = (
    df.groupby("SKU")["Revenue (€)"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

abc["Revenue %"] = (
    abc["Revenue (€)"] /
    abc["Revenue (€)"].sum()
) * 100

abc["Cumulative %"] = abc["Revenue %"].cumsum()


def abc_category(value):

    if value <= 80:
        return "A"

    elif value <= 95:
        return "B"

    else:
        return "C"


abc["ABC Class"] = abc["Cumulative %"].apply(abc_category)


fig_abc = px.bar(
    abc.head(30),
    x="SKU",
    y="Revenue (€)",
    color="ABC Class",
    title="ABC Analysis – Top Products"
)

st.plotly_chart(
    fig_abc,
    use_container_width=True
)


a_count = (abc["ABC Class"] == "A").sum()
b_count = (abc["ABC Class"] == "B").sum()
c_count = (abc["ABC Class"] == "C").sum()

a, b, c = st.columns(3)

with a:
    st.metric("A Products", a_count)

with b:
    st.metric("B Products", b_count)

with c:
    st.metric("C Products", c_count)

st.dataframe(
    abc,
    use_container_width=True
)


# ---------------------------------------------------------
# PARETO / PARITY ANALYSIS
# ---------------------------------------------------------

st.header("📊 8. Pareto / Parity Analysis")

st.markdown("""
Pareto analysis identifies the small number of products that
generate a large proportion of total revenue.

This follows the **80/20 principle** as an analytical guideline,
not as a forced assumption.
""")

pareto = (
    df.groupby("SKU")["Revenue (€)"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

pareto["Cumulative Revenue %"] = (
    pareto["Revenue (€)"].cumsum() /
    pareto["Revenue (€)"].sum()
) * 100

fig_pareto = px.line(
    pareto,
    x="SKU",
    y="Cumulative Revenue %",
    title="Pareto Analysis – Cumulative Revenue"
)

fig_pareto.add_hline(
    y=80,
    line_dash="dash",
    annotation_text="80% Revenue"
)

st.plotly_chart(
    fig_pareto,
    use_container_width=True
)


# ---------------------------------------------------------
# PRODUCT VS QUANTITY
# ---------------------------------------------------------

st.header("⚖️ 9. Product vs Quantity Analysis")

product_quantity = (
    df.groupby("SKU")
    .agg(
        Revenue=("Revenue (€)", "sum"),
        Quantity=("Sales Quantity", "sum")
    )
    .reset_index()
)

fig_scatter = px.scatter(
    product_quantity,
    x="Quantity",
    y="Revenue",
    hover_name="SKU",
    title="Sales Quantity vs Revenue",
    trendline="ols"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)


# ---------------------------------------------------------
# CATEGORY ANALYSIS
# ---------------------------------------------------------

st.header("🏷️ 10. Category-Based Business Analysis")

category_analysis = (
    df.groupby("Category")
    .agg(
        Revenue=("Revenue (€)", "sum"),
        Quantity=("Sales Quantity", "sum")
    )
    .sort_values("Revenue", ascending=False)
    .reset_index()
)

fig_category = px.bar(
    category_analysis,
    x="Category",
    y="Revenue",
    title="Revenue by Product Category"
)

st.plotly_chart(
    fig_category,
    use_container_width=True
)


# ---------------------------------------------------------
# BUSINESS MODEL / DECISION SUPPORT
# ---------------------------------------------------------

st.header("🚀 11. Business Model Recommendations")

total_revenue = df["Revenue (€)"].sum()

top_product = (
    df.groupby("SKU")["Revenue (€)"]
    .sum()
    .sort_values(ascending=False)
)

top_category = (
    df.groupby("Category")["Revenue (€)"]
    .sum()
    .sort_values(ascending=False)
)

top_supplier = (
    df.groupby("Supplier")["Revenue (€)"]
    .sum()
    .sort_values(ascending=False)
)


st.subheader("📌 Data-Driven Recommendations")

st.write(
    f"**1. Focus on high-value products:** "
    f"{top_product.index[0]} is the highest-revenue SKU."
)

st.write(
    f"**2. Prioritise the leading category:** "
    f"{top_category.index[0]} generates the highest category revenue."
)

st.write(
    f"**3. Supplier strategy:** "
    f"{top_supplier.index[0]} is the highest-revenue supplier."
)

st.write(
    "**4. Inventory strategy:** "
    "A-class products should receive the highest monitoring priority."
)

st.write(
    "**5. Business strategy:** "
    "Use demand forecasting together with ABC analysis to decide "
    "which products should receive additional inventory investment."
)


# ---------------------------------------------------------
# EXECUTIVE SUMMARY
# ---------------------------------------------------------

st.header("📋 Executive Summary")

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.metric(
        "Revenue",
        f"€{total_revenue:,.0f}"
    )

with s2:
    st.metric(
        "Products",
        f"{df['SKU'].nunique():,}"
    )

with s3:
    st.metric(
        "Categories",
        f"{df['Category'].nunique():,}"
    )

with s4:
    st.metric(
        "Suppliers",
        f"{df['Supplier'].nunique():,}"
    )

st.success(
    "✅ Business Analytics completed. "
    "Use these results to support product, inventory, "
    "supplier and revenue decisions."
)