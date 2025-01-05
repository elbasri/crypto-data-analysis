import pandas as pd
import os
from config import API_KEY, SECRET_KEY

# Load historical price data for the top 10 pairs
input_dir = "data/binance/top_10/"
top_10_files = [f for f in os.listdir(input_dir) if f.endswith("_history_last_year.csv")]

# Prepare a DataFrame for closing prices
price_data = pd.DataFrame()
for file in top_10_files:
    symbol = file.split("_")[0]
    data = pd.read_csv(os.path.join(input_dir, file))
    price_data[symbol] = data["Close"]

# Calculate correlation matrix
correlation_matrix = price_data.corr()

# Save to CSV
output_file = "data/binance/top_10_correlation_matrix.csv"
correlation_matrix.to_csv(output_file)
print(f"Saved correlation matrix to {output_file}")
