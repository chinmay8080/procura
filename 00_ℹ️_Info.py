import streamlit as st

pages = [
    st.Page("info_page.py", title="Overview", icon="ℹ️", default=True),
    st.Page("01_1️⃣_Forecast_Demand.py", title="Demand Forecasting", icon="📊"),
    st.Page("02_2️⃣_Inventory_Optimisation.py", title="Inventory Optimisation", icon="📦"),
    st.Page("03_3️⃣_Customer_Product_Segmentation.py", title="Customer & Product Segmentation", icon="👥"),
    st.Page("04_4️⃣_Statistical_Tests.py", title="Statistical Tests", icon="🧮"),
    st.Page("05_5️⃣_EDA_Insights.py", title="EDA Insights", icon="📈"),
]

page = st.navigation(pages)
page.run()