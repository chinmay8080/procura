from pathlib import Path

import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    data_path = Path(__file__).resolve().parent / "pharmaceutical_supply_chain.csv.gz"
    return pd.read_csv(data_path, parse_dates=["Date"])