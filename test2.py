import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates

#pip install mplfinance
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

# Convert dates to matplotlib format
df['Date'] = df['Date'].apply(mdates.date2num)

# Create a subplot
fig, ax = plt.subplots()

# Plot the OHLC data
candlestick_ohlc(ax, df.values, width=0.6, colorup='g', colordown='r')

# Set x-axis format
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

plt.title('OHLC Graph')
plt.xlabel('Date')
plt.ylabel('Price')
plt.tight_layout()

# Show the plot
plt.show()
