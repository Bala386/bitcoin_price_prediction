import plotly.graph_objects as go
import pandas as pd

# Sample data
data = {
    'Date': ['2024-04-01', '2024-04-02', '2024-04-03', '2024-04-04', '2024-04-05'],
    'Open': [100, 102, 98, 105, 103],
    'High': [105, 110, 100, 112, 106],
    'Low': [97, 98, 95, 100, 98],
    'Close': [102, 108, 97, 110, 100]
}

# Convert 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Create a DataFrame
df = pd.DataFrame(data)

# Create an OHLC plot
fig = go.Figure(data=go.Ohlc(x=df['Date'],
                              open=df['Open'],
                              high=df['High'],
                              low=df['Low'],
                              close=df['Close']))

# Customize layout
fig.update_layout(
    title='OHLC Graph',
    xaxis_title='Date',
    yaxis_title='Price'
)

# Show plot
fig.show()
