import matplotlib.pyplot as plt
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

# Create and display the plot in the main thread
def display_plot():
    fig, ax = plt.subplots()
    ax.plot(df['Date'], df['Close'])
    plt.show()

# Call the function to display the plot
display_plot()
