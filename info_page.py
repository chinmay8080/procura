import streamlit as st

st.set_page_config(page_title="Procura", page_icon="🔮", layout="wide")

st.title("Replica Health LTD: Supply Chain Data Modelling")

st.markdown("""
Replica Health Supply Chain Data Modelling is a powerful analytical tool designed to explore,
visualise, and model data specific to supply chain management in the healthcare and pharmaceutical industry.
This app provides detailed insights into inventory, sales, customer segmentation, product performance, and more.

### About the Dataset
The dataset used in this application has been **synthetically generated** using Python and a Jupyter Notebook.
The primary purpose of using a synthetic dataset is to create realistic yet fictional data to simulate real-world
supply chain scenarios without the need for sensitive or proprietary information.

Here are the key steps taken to generate this dataset:
""")

st.markdown("""
#### 1️⃣ Product Details Generation
- **Number of Products (SKUs):** 380 unique SKUs.
- **Categories:** Products belong to categories like **Prescription Drugs**, **Vaccines**, **Diagnostics**, and more.
- **Suppliers:** Five major suppliers: *PharmaCorp*, *MediSupply*, *HealthPlus*, *BioGen*, and *Cardinal Med*.
- **Product Family Names:** Examples include *Pain Reliever*, *COVID-19 Vaccine*, *Antibiotic*, and others.

#### 2️⃣ Customer Data Creation
- **Number of Customers:** 50 unique customers generated.
- **High-Volume Customers:** 30% of customers are assigned as high-volume buyers, consuming higher quantities.

#### 3️⃣ Time-Series Sales Data
- **Date Range:** From **1st January 2018** to **today**.
- **Seasonality Patterns:** Sales quantities vary based on structured seasonal demand patterns.
- **Trend Factor:** A gradual growth in demand over time is simulated.
- **Lead Time:** Random delays in supply chain logistics with lead times between 1 and 10 days.

#### 4️⃣ Sales and Inventory Data
- **Stock Levels:** Randomly generated for each SKU and adjusted based on demand.
- **Sales Quantity and Revenue:** Calculated using the product price and customer purchasing behavior.

#### 5️⃣ Dataset Composition
- After generating sales data, it was merged with product details to create a comprehensive dataset.
- The final dataset includes **columns** like:
  - `Date`, `SKU`, `Customer ID`, `Stock Level`, `Sales Quantity`, `Revenue (€)`, and `Lead Time (days)`.

### Why Use a Synthetic Dataset?
The synthetic dataset allows us to:
1. Simulate realistic supply chain scenarios for testing and visualisation.
2. Maintain privacy and confidentiality by avoiding the use of real-world data.
3. Experiment freely with statistical and machine learning models for research purposes.

### Key Features of the App
1. **Demand Forecasting:** Predict future demand using time series and machine learning models.
2. **Inventory Optimisation:** Calculate metrics like Economic Order Quantity (EOQ), Safety Stock, and Monte Carlo Simulation.
3. **Customer and Product Segmentation:** Analise sales performance by product, customer, and category.
4. **Statistical Testing:** Perform hypothesis testing to identify key factors affecting sales and revenue.

We hope you enjoy exploring and analysing the dataset! 🚀
""")

st.markdown("""
---

### Generated Dataset File
The dataset generated through this process has been saved as **`pharmaceutical_supply_chain.csv`**
and is used throughout this app.
""")