import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from keras.models import Sequential
from keras.layers import Dense, LSTM

def get_bitcoin_data():
    import yfinance as yf
    data = yf.download("BTC-USD", start="2016-01-01", end="2024-12-31")
    return data

def prepare_lstm_data(data, n_steps=60):
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1,1))

    X, y = [], []
    for i in range(n_steps, len(scaled_data)):
        X.append(scaled_data[i-n_steps:i, 0])
        y.append(scaled_data[i, 0])
    X, y = np.array(X), np.array(y)
    return X.reshape(X.shape[0], X.shape[1], 1), y, scaler

def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(units=50))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

def train_linear_model(data):
    data['Prediction'] = data['Close'].shift(-1)
    X = data[['Close']][:-1]
    y = data['Prediction'][:-1]
    model = LinearRegression()
    model.fit(X, y)
    return model