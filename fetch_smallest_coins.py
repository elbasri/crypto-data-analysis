import pandas as pd

# Load the trading pairs information file
data_path = "data/binance/usdt_trading_pairs_info-10-01-2025.csv"
trading_pairs_info = pd.read_csv(data_path)

# Ensure the required columns are present
required_columns = ["Symbol", "Min Price", "Max Qty"]
if not all(col in trading_pairs_info.columns for col in required_columns):
    raise ValueError(f"The file must contain the following columns: {required_columns}")

# Filter for trading pairs with 'TRADING' status
trading_pairs_info = trading_pairs_info[trading_pairs_info['Status'] == 'TRADING']

# Convert 'Min Price' and 'Max Qty' to numeric
trading_pairs_info['Min Price'] = pd.to_numeric(trading_pairs_info['Min Price'], errors='coerce')
trading_pairs_info['Max Qty'] = pd.to_numeric(trading_pairs_info['Max Qty'], errors='coerce')

# Drop rows with missing values in the relevant columns
trading_pairs_info = trading_pairs_info.dropna(subset=['Min Price', 'Max Qty'])

# Calculate a score based on the lowest price and highest volume (Max Qty)
trading_pairs_info['Score'] = trading_pairs_info['Max Qty'] / trading_pairs_info['Min Price']

# Sort by the score in descending order and select the top 50 pairs
top_50_pairs = trading_pairs_info.sort_values(by='Score', ascending=False).head(50)

# Save the top 50 pairs to a new CSV file
output_file = "data/binance/top_50_usdt_pairs_by_price_volume.csv"
top_50_pairs.to_csv(output_file, index=False)

print(f"Top 50 USDT trading pairs with lowest price and highest volume saved to {output_file}")
