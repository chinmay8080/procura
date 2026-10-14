# 🚀 Procura

**Procura** is a Streamlit-based analytics platform designed to provide **advanced analytics** and **data modelling** for **pharmaceutical supply chain management**.

The application enables users to perform **demand forecasting**, **inventory optimisation**, **customer & product segmentation**, and **statistical hypothesis testing** to support data-driven decision-making in supply chain operations.

---

# 📂 Project Structure

```text
SupplyChainDataModellingStreamlit
│
├── .streamlit/
│   └── config.toml
│
├── assets/
│   └── data/
│       ├── DataGenerator.ipynb
│       └── pharmaceutical_supply_chain.csv
│
├── streamlit_app/
│   ├── pages/
│   │   ├── 01_Forecast_Demand.py
│   │   ├── 02_Inventory_Optimisation.py
│   │   ├── 03_Customer_Product_Segmentation.py
│   │   └── 04_Hypothesis_Testing.py
│   │
│   └── 00_Info.py
│
├── LICENSE
├── README.md
└── requirements.txt
```

---

# 🛠️ Features of the App

The application consists of **four key modules**, each designed to address specific supply chain challenges.

---

## 1️⃣ Demand Forecasting using LSTM

### 📌 What does it do?

- Uses an **LSTM (Long Short-Term Memory)** neural network to forecast future demand.
- Allows users to select a specific **SKU** and generate a **one-year demand forecast**.
- Helps businesses anticipate future sales trends and improve planning.

### ⚙️ How does it work?

- Preprocesses historical sales data.
- Removes non-stationarity and smooths demand fluctuations.
- Uses an **80%-20% train-test split** for validation.
- Trains an LSTM model to learn historical demand patterns.

### 📊 Output

- Interactive demand forecast visualization.
- Historical vs predicted demand comparison.
- **Mean Absolute Percentage Error (MAPE)** for accuracy evaluation.
- Downloadable forecast results.

---

## 2️⃣ Inventory Optimisation & Simulation

### 📌 What does it do?

Provides inventory planning support using:

- **Economic Order Quantity (EOQ)** – Determines the optimal order quantity.
- **Safety Stock Calculation** – Prevents stockouts and service disruptions.
- **Monte Carlo Simulation** – Models demand uncertainty and risk.

### ⚙️ How does it work?

- Users select an SKU.
- Inventory parameters are calculated automatically.
- Generates **1000+ simulated demand scenarios** using random sampling techniques.

### 📊 Output

- EOQ and Safety Stock tables.
- Demand distribution plots.
- Interactive inventory risk analysis visualizations.

---

## 3️⃣ Customer & Product Segmentation

### 📌 What does it do?

Provides insights into customer and product performance.

Users can explore:

- **Sales by Supplier**
- **Sales by Product Family**
- **Sales by Product Category**
- **Top & Bottom Customers**
- **Stock Turnover Analysis**

### ⚙️ How does it work?

- Aggregates sales and revenue metrics.
- Calculates inventory turnover ratios.
- Visualizes supplier, customer, and product performance using interactive charts.

### 📊 Output

- Top and bottom 20 products by sales.
- Stock turnover rankings.
- Supplier performance dashboards.
- Customer segmentation reports.

---

## 4️⃣ Statistical Hypothesis Testing

### 📌 What does it do?

Performs statistical tests to validate important supply chain assumptions.

### 🔬 Available Tests

#### 1. Stockouts Reduce Sales
- Pearson Correlation between stock levels and sales.

#### 2. Longer Lead Times Lower Sales
- Linear Regression between lead time and sales.

#### 3. Supplier Revenue Differs Significantly
- Kruskal-Wallis Test across suppliers.

#### 4. Frequent Buyers Generate More Revenue
- Spearman Correlation between purchase frequency and revenue.

#### 5. Certain Product Categories Generate Higher Revenue
- ANOVA Test across product categories.

### ⚙️ How does it work?

- Users select a hypothesis from a dropdown menu.
- Statistical calculations are performed automatically.
- Test distributions and rejection regions are visualized.

### 📊 Output

- Test statistics.
- P-values.
- Accept/Reject decision for the null hypothesis.
- Graphical interpretation of results.

---

# 🎯 Why Use Procura?

✅ **Realistic Data Analysis** – Built using a synthetic pharmaceutical supply chain dataset.

✅ **End-to-End Workflow** – Covers forecasting, inventory planning, segmentation, and hypothesis testing.

✅ **Business-Driven Insights** – Helps identify demand trends, supplier performance, and customer behaviour.

✅ **Interactive Visualisations** – Simplifies complex supply chain analysis.

✅ **User-Friendly Interface** – Designed for quick and intuitive exploration.

---

# 🧰 Tech Stack

- **Python**
- **Streamlit**
- **Pandas**
- **NumPy**
- **TensorFlow / Keras**
- **Scikit-learn**
- **SciPy**
- **Plotly**
- **Matplotlib**

---
# 📈 Business Value

Procura helps supply chain professionals:

- Forecast future product demand accurately.
- Optimise inventory levels and reduce holding costs.
- Identify high-value customers and products.
- Analyse supplier performance.
- Validate business assumptions using statistical testing.
- Support data-driven decision-making.
