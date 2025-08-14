import streamlit as st
import matplotlib.pyplot as plt
from model_utils import get_bitcoin_data, prepare_lstm_data, build_lstm_model, train_linear_model
import numpy as np

st.title("📈 Bitcoin Price Prediction using ML & Deep Learning")

# Load data
data = get_bitcoin_data()
st.subheader("Bitcoin Price Chart")
st.line_chart(data['Close'])

# Select algorithm
option = st.selectbox("Choose Prediction Algorithm", ["Linear Regression", "LSTM (Deep Learning)"])

if option == "Linear Regression":
    model = train_linear_model(data)
    future_price = model.predict([[data['Close'].iloc[-1]]])[0]
    st.success(f"📉 Next day's predicted price: ${future_price:.2f}")

elif option == "LSTM (Deep Learning)":
    st.write("Training LSTM Model (takes ~10 sec)...")
    X, y, scaler = prepare_lstm_data(data)
    model = build_lstm_model((X.shape[1], 1))
    model.fit(X, y, epochs=5, batch_size=32, verbose=0)

    last_sequence = X[-1].reshape(1, X.shape[1], 1)
    predicted_scaled = model.predict(last_sequence)
    predicted_price = scaler.inverse_transform(predicted_scaled)[0][0]

    st.success(f"🧠 LSTM Predicted Next Price: ${predicted_price:.2f}")

# Plot actual vs predicted chart
st.subheader("Prediction Comparison")
st.line_chart(data['Close'].tail(100))