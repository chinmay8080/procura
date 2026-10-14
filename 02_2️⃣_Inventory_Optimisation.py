import numpy as np
import pandas as pd
import streamlit as st
from data_utils import load_data
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats

# Set Streamlit page config
st.set_page_config(page_title="Inventory Optimisation", page_icon="📦",layout="wide")

# Add Sidebar Explanations
st.sidebar.header("ℹ️ About the Tests")
st.sidebar.markdown(
    """
    ### What Are We Doing Here?
    This tool performs the following calculations to optimise inventory:
    """
)

st.sidebar.markdown("#### 1️⃣ **Economic Order Quantity (EOQ):**")
st.sidebar.markdown(
    """
    - Determines the optimal order quantity that minimises total inventory costs (ordering + holding).
    """
)
st.sidebar.latex(r"EOQ = \sqrt{\frac{2 \times Demand \times Ordering\ Cost}{Holding\ Cost}}")

st.sidebar.markdown("#### 2️⃣ **Safety Stock:**")
st.sidebar.markdown(
    """
    - Calculates extra stock to hold to prevent stockouts during demand or lead time variability.
    - Here, **Z** is a service level factor (default: 95% confidence).
    """
)
st.sidebar.latex(r"Safety\ Stock = Z \times Std\ Dev\ of\ Demand \times \sqrt{Lead\ Time}")

st.sidebar.markdown("#### 3️⃣ **Monte Carlo Simulation:**")
st.sidebar.markdown(
    """
    - Uses simulated random demand data to predict future variations in demand.
    - Outputs a histogram showing the distribution of simulated average demand.
    """
)


# Load dataset
df = load_data()

# Aggregate demand per SKU and calculate key inventory parameters
df_grouped = df.groupby("SKU").agg(
    avg_demand=('Sales Quantity', 'mean'),
    std_demand=('Sales Quantity', 'std'),
    avg_lead_time=('Lead Time (days)', 'mean')
).reset_index()

# 📌 **1️⃣ Economic Order Quantity (EOQ) Calculation**
def calculate_eoq(demand, ordering_cost, holding_cost):
    """ EOQ Formula: sqrt((2 * Demand * Ordering Cost) / Holding Cost) """
    return round(np.sqrt((2 * demand * ordering_cost) / holding_cost), 2)

# Set static cost assumptions
ordering_cost = 50  # Cost per order
holding_cost = 2  # Cost per unit per year

# Apply EOQ for each SKU
df_grouped["EOQ"] = df_grouped.apply(lambda row: calculate_eoq(row["avg_demand"], ordering_cost, holding_cost), axis=1)

# 📌 **2️⃣ Safety Stock Calculation**
def calculate_safety_stock(std_dev_demand, lead_time_days, service_level=0.95):
    """ Safety Stock Formula: Z * Std Dev of Demand * sqrt(Lead Time Days) """
    z_score = stats.norm.ppf(service_level)  # Get Z-score for desired service level
    return round(z_score * std_dev_demand * np.sqrt(lead_time_days), 2)

# Apply Safety Stock Calculation
df_grouped["Safety Stock"] = df_grouped.apply(lambda row: calculate_safety_stock(row["std_demand"], row["avg_lead_time"]), axis=1)

# 📌 **3️⃣ Monte Carlo Simulation for Future Demand**
def monte_carlo_simulation(sku_data, num_simulations=1000, days=30):
    """ Simulates demand variations over time using normal distribution """
    simulated_demands = np.random.normal(sku_data["avg_demand"], sku_data["std_demand"], (num_simulations, days))

    # Prepare data for visualisation
    simulated_means = simulated_demands.mean(axis=1)

    # Create Plotly histogram for the simulated demand
    fig = px.histogram(
        simulated_means,
        nbins=30,
        title=f"Monte Carlo Simulation: Demand Distribution for {sku_data['SKU']}",
        labels={'value': 'Demand'},
        opacity=0.75
    )
    fig.update_layout(
        xaxis_title="Simulated Average Demand",
        yaxis_title="Frequency",
        template="plotly_white"
    )
    st.plotly_chart(fig)

    return simulated_demands

# Streamlit UI
st.title("Inventory Optimisation Tool")
st.subheader("Optimise Inventory Parameters")

# Display Key Inventory Parameters
st.markdown("### Key Inventory Parameters for Each SKU:")
st.dataframe(df_grouped[["SKU", "EOQ", "Safety Stock"]].set_index("SKU"))

# Select a sample SKU for Monte Carlo Simulation
st.markdown("### Monte Carlo Simulation")
sample_sku = st.selectbox("Select an SKU for Demand Simulation:", df_grouped["SKU"])
selected_data = df_grouped[df_grouped["SKU"] == sample_sku].iloc[0]  # Get selected SKU data

# Run Monte Carlo Simulation
st.markdown("Simulating future demand variations...")
simulated_data = monte_carlo_simulation(selected_data)

# Display Results
st.markdown(f"Simulation completed for SKU **{sample_sku}**!")
