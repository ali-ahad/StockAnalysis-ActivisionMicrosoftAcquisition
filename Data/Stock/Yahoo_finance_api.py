import yfinance as yf
import pandas as pd

# List of stock symbols (MSFT, ATVI, etc.)
stocks = ['MSFT']  # Add more stock symbols as needed

# Initialize a list to store DataFrame objects
dataframes = []

for stock in stocks:
    # Fetch historical data
    data = yf.download(stock, start='2018-11-01', end='2018-12-01')

    # Add a symbol column
    data['Symbol'] = stock

    # Append the DataFrame to the list
    dataframes.append(data)

# Concatenate all DataFrame objects in the list
all_data = pd.concat(dataframes)

# Reset index to get Date as a column
all_data = all_data.reset_index()

# Select and rename columns
all_data = all_data[['Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume']]

# Save to CSV
all_data.to_csv('stock_data.csv', index=False)
