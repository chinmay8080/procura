import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import streamlit as st
from data_utils import load_data
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_percentage_error
from statsmodels.tsa.stattools import adfuller
import plotly.graph_objects as go

# Set Streamlit page config
st.set_page_config(page_title="Forecast Future Demand",page_icon="📊", layout="wide")

# Load dataset
df = load_data()

# Sidebar for SKU selection
st.sidebar.header("Select SKU to Forecast")
sku_list = df["SKU"].unique()
selected_sku = st.sidebar.selectbox("Choose SKU:", sku_list)

# Add user instructions
st.sidebar.markdown(
    """
    ### Instructions:
    1. Select the SKU you want to forecast from the dropdown menu.
    2. Click the **"Train Model and Forecast"** button to begin.
    3. Please note that the process may take some time to complete. Be patient!
    """
)

# Add a button on the sidebar to trigger training
if st.sidebar.button("Train Model and Forecast"):
    from keras.callbacks import EarlyStopping
    from keras.models import Sequential
    from keras.layers import Input, LSTM, Dense, Dropout
    from keras.optimizers import Adam

    # Filter data for selected SKU
    df_sku = df[df["SKU"] == selected_sku]
    df_forecast = df_sku.groupby("Date")["Sales Quantity"].sum().reset_index()
    df_forecast.set_index("Date", inplace=True)

    # ADF Test for stationarity
    def check_stationarity(timeseries):
        result = adfuller(timeseries)
        return timeseries if result[1] <= 0.05 else timeseries.diff().dropna()

    df_forecast["Sales Quantity"] = check_stationarity(df_forecast["Sales Quantity"])
    df_forecast = df_forecast.resample('W').sum()  # Weekly aggregation
    df_forecast["Rolling Sales"] = df_forecast["Sales Quantity"].rolling(window=4, min_periods=1).mean()
    df_forecast.dropna(subset=["Rolling Sales"], inplace=True)

    # Normalize data
    scaler = MinMaxScaler()
    df_forecast["Sales Quantity Scaled"] = scaler.fit_transform(df_forecast[["Rolling Sales"]])

    # Train-Test Split
    split_idx = int(len(df_forecast) * 0.8)
    train_data = df_forecast.iloc[:split_idx]
    test_data = df_forecast.iloc[split_idx:]

    # Function to create LSTM data
    def create_lstm_data(series, time_steps):
        X, y = [], []
        for i in range(len(series) - time_steps):
            X.append(series[i: i + time_steps])
            y.append(series[i + time_steps])
        return np.array(X), np.array(y)

    # Prepare training and test data
    time_steps = 24
    train_series = train_data["Sales Quantity Scaled"].values
    test_series = test_data["Sales Quantity Scaled"].values

    X_train, y_train = create_lstm_data(train_series, time_steps)
    X_test, y_test = create_lstm_data(test_series, time_steps)

    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

    # Define LSTM Model
    def build_lstm():
        model = Sequential([
            Input(shape=(time_steps, 1)),
            LSTM(32, return_sequences=True),
            Dropout(0.2),
            LSTM(16),
            Dense(1)
        ])
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
        return model

    lstm_model = build_lstm()
    lstm_model.fit(
        X_train,
        y_train,
        epochs=40,
        batch_size=32,
        verbose=0,
        callbacks=[EarlyStopping(monitor="loss", patience=5, restore_best_weights=True)],
    )

    # Generate Forecast
    lstm_predictions = lstm_model.predict(X_test, verbose=0)
    lstm_predictions = scaler.inverse_transform(lstm_predictions)

    # Align forecasted values
    pred_series_lstm = pd.Series(lstm_predictions.flatten(), index=test_data.index[time_steps:])

    # Compute Accuracy (MAPE)
    mape_lstm = mean_absolute_percentage_error(test_data["Rolling Sales"].iloc[time_steps:], pred_series_lstm)

    # Future Forecast (52 weeks)
    forecast_steps = 52
    lstm_forecast = []
    last_data = test_data["Sales Quantity Scaled"].values[-time_steps:]

    for _ in range(forecast_steps):
        input_data = last_data.reshape((1, time_steps, 1))
        pred = float(lstm_model(input_data, training=False).numpy()[0, 0])
        lstm_forecast.append(pred)
        last_data = np.append(last_data[1:], pred)

    # Convert predictions back to original scale
    lstm_forecast = scaler.inverse_transform(np.array(lstm_forecast).reshape(-1, 1))
    forecast_dates = pd.date_range(test_data.index[-1], periods=forecast_steps + 1, freq='W')[1:]
    pred_series_future = pd.Series(lstm_forecast.flatten(), index=forecast_dates)

    # Streamlit UI
    st.subheader(f"LSTM Model Forecast for {selected_sku}")

    # Display MAPE
    st.metric("LSTM Forecast Accuracy (MAPE)", f"{mape_lstm * 100:.2f} %")

    # Plot Sales Forecast using Plotly
    fig = go.Figure()

    # Train data
    fig.add_trace(go.Scatter(
        x=train_data.index,
        y=train_data["Rolling Sales"],
        mode='lines',
        name='Train Data',
        line=dict(color='blue', width=2)
    ))

    # Transition between train-test
    fig.add_trace(go.Scatter(
        x=[train_data.index[-1], test_data.index[0]],
        y=[train_data["Rolling Sales"].iloc[-1], test_data["Rolling Sales"].iloc[0]],
        mode='lines',
        line=dict(color='blue', dash='dash'),
        showlegend=False
    ))

    # Test data
    fig.add_trace(go.Scatter(
        x=test_data.index,
        y=test_data["Rolling Sales"],
        mode='lines',
        name='Test Data',
        line=dict(color='green', width=2)
    ))

    # LSTM predictions
    fig.add_trace(go.Scatter(
        x=pred_series_lstm.index,
        y=pred_series_lstm,
        mode='lines',
        name='LSTM Predictions',
        line=dict(color='red', dash='dash')
    ))

    # Future forecast
    fig.add_trace(go.Scatter(
        x=pred_series_future.index,
        y=pred_series_future,
        mode='lines',
        name='Future Forecast',
        line=dict(color='purple', dash='dot')
    ))

    # Layout and labels
    fig.update_layout(
        title=f"1-Year LSTM Forecast for {selected_sku}",
        xaxis_title="Date",
        yaxis_title="Sales Quantity",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white"
    )

    st.plotly_chart(fig)

    # Display Forecast Data
    st.subheader("Forecasted Sales Data")
    forecast_df = pd.DataFrame({"Date": pred_series_future.index, "Predicted Sales": pred_series_future.values})
    st.dataframe(forecast_df.set_index("Date"))
