from binance.client import Client
import csv
import os
from config import API_KEY, SECRET_KEY

# Initialize Binance Client
client = Client(API_KEY, SECRET_KEY)

# Load top 10 pairs from the CSV file
input_file = "data/binance/top_10_usdt_pairs_with_info.csv"
top_10_usdt_pairs = []

with open(input_file, mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        top_10_usdt_pairs.append(row["Symbol"])

# Directory to save aggregated trades
output_dir = "data/binance/top_10_aggregated_trades/"
os.makedirs(output_dir, exist_ok=True)

# Fetch and save aggregated trade data
for symbol in top_10_usdt_pairs:
    print(f"Fetching aggregated trades for {symbol}...")
    try:
        trades = client.get_aggregate_trades(symbol=symbol, limit=1000)
        output_file = os.path.join(output_dir, f"{symbol}_aggregated_trades.csv")
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Trade ID", "Price", "Quantity", "First Trade ID", "Last Trade ID", "Time"])
            for trade in trades:
                writer.writerow([trade['a'], trade['p'], trade['q'], trade['f'], trade['l'], trade['T']])
        print(f"Saved aggregated trades for {symbol} to {output_file}")
    except Exception as e:
        print(f"Error fetching aggregated trades for {symbol}: {e}")
