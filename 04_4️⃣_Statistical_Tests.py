import streamlit as st
from data_utils import load_data
import numpy as np
import pandas as pd
import scipy.stats as stats
from sklearn.linear_model import LinearRegression

# Set Streamlit page config
st.set_page_config(page_title="Statistical Tests",page_icon="🧮", layout="wide")

# Load dataset
df = load_data()

# Significance level
alpha = 0.05

# Sidebar for selecting the test
st.sidebar.header("Select Statistical Test")
test_options = [
    "Stockouts reduce sales (Pearson Correlation)",
    "Longer lead times lower sales (Linear Regression)",
    "Supplier revenue distribution (Kruskal-Wallis Test)",
    "Frequent buyers generate higher revenue (Spearman Correlation)",
    "Certain categories generate higher revenue (ANOVA)"
]
selected_test = st.sidebar.selectbox("Choose a test to perform:", test_options)

# Explanations and Tests
if selected_test == "Stockouts reduce sales (Pearson Correlation)":
    st.title("Stockouts Reduce Sales (Pearson Correlation)")
    st.markdown("""
    **Hypothesis:**
    - **H₀**: There is no significant linear relationship between stock level and sales quantity.
    - **H₁**: Stock level significantly affects sales quantity.
    
    **Why this test?**
    - Pearson Correlation is suitable for evaluating the **linear relationship** between two continuous variables: stock level and sales quantity.
    """)

    # Perform Pearson Correlation
    pearson_corr, p_value_pearson = stats.pearsonr(df["Stock Level"], df["Sales Quantity"])
    decision = "Reject H₀" if p_value_pearson < alpha else "Fail to Reject H₀"

    # Display results
    st.write(f"**Correlation Coefficient (r):** {pearson_corr:.4f}")
    st.write(f"**P-value:** {p_value_pearson:.4f}")
    st.write(f"**Decision:** {decision}")

elif selected_test == "Longer lead times lower sales (Linear Regression)":
    st.title("Longer Lead Times Lower Sales (Linear Regression)")
    st.markdown("""
    **Hypothesis:**
    - **H₀**: Lead time has no significant impact on sales quantity.
    - **H₁**: Lead time significantly affects sales quantity.
    
    **Why this test?**
    - Linear Regression models the relationship between **lead time (continuous)** and **sales quantity (continuous)**.
    """)

    # Perform Linear Regression
    X = df["Lead Time (days)"].values.reshape(-1, 1)
    y = df["Sales Quantity"].values
    reg_model = LinearRegression().fit(X, y)
    r_squared = reg_model.score(X, y)  # R² value
    p_value_reg = stats.pearsonr(df["Lead Time (days)"], df["Sales Quantity"])[1]  # p-value via correlation
    decision = "Reject H₀" if p_value_reg < alpha else "Fail to Reject H₀"

    # Display results
    st.write(f"**R² (Coefficient of Determination):** {r_squared:.4f}")
    st.write(f"**P-value:** {p_value_reg:.4f}")
    st.write(f"**Decision:** {decision}")

elif selected_test == "Supplier revenue distribution (Kruskal-Wallis Test)":
    st.title("Supplier Revenue Distribution (Kruskal-Wallis Test)")
    st.markdown("""
    **Hypothesis:**
    - **H₀**: Revenue is evenly distributed among suppliers.
    - **H₁**: Revenue is unevenly distributed among suppliers.
    
    **Why this test?**
    - Kruskal-Wallis is a **non-parametric test** for comparing multiple independent groups (suppliers in this case).
    """)

    # Perform Kruskal-Wallis Test
    supplier_revenue_groups = [df[df["Supplier"] == supplier]["Revenue (€)"] for supplier in df["Supplier"].unique()]
    kruskal_stat, p_value_kruskal = stats.kruskal(*supplier_revenue_groups)
    decision = "Reject H₀" if p_value_kruskal < alpha else "Fail to Reject H₀"

    # Display results
    st.write(f"**Kruskal-Wallis Statistic:** {kruskal_stat:.4f}")
    st.write(f"**P-value:** {p_value_kruskal:.4f}")
    st.write(f"**Decision:** {decision}")

elif selected_test == "Frequent buyers generate higher revenue (Spearman Correlation)":
    st.title("Frequent Buyers Generate Higher Revenue (Spearman Correlation)")
    st.markdown("""
    **Hypothesis:**
    - **H₀**: Purchase frequency has no significant monotonic relationship with revenue.
    - **H₁**: Purchase frequency has a significant monotonic relationship with revenue.
    
    **Why this test?**
    - Spearman Correlation is used to evaluate **monotonic relationships** between frequency and revenue.
    """)

    # Perform Spearman Correlation
    customer_rfm = df.groupby("Customer ID").agg({"Customer ID": "count", "Revenue (€)": "sum"})
    customer_rfm.columns = ["Frequency", "Monetary"]
    spearman_corr, p_value_spearman = stats.spearmanr(customer_rfm["Frequency"], customer_rfm["Monetary"])
    decision = "Reject H₀" if p_value_spearman < alpha else "Fail to Reject H₀"

    # Display results
    st.write(f"**Spearman Correlation Coefficient (ρ):** {spearman_corr:.4f}")
    st.write(f"**P-value:** {p_value_spearman:.4f}")
    st.write(f"**Decision:** {decision}")

elif selected_test == "Certain categories generate higher revenue (ANOVA)":
    st.title("Certain Categories Generate Higher Revenue (ANOVA)")
    st.markdown("""
    **Hypothesis:**
    - **H₀**: All product categories generate similar revenue.
    - **H₁**: Certain product categories generate significantly different revenue.
    
    **Why this test?**
    - ANOVA is suitable for comparing **mean revenues** across multiple groups (categories in this case).
    """)

    # Perform ANOVA
    category_revenue_groups = [df[df["Category"] == category]["Revenue (€)"] for category in df["Category"].unique()]
    f_stat_category, p_value_category = stats.f_oneway(*category_revenue_groups)
    decision = "Reject H₀" if p_value_category < alpha else "Fail to Reject H₀"

    # Display results
    st.write(f"**F-Statistic:** {f_stat_category:.4f}")
    st.write(f"**P-value:** {p_value_category:.4f}")
    st.write(f"**Decision:** {decision}")
