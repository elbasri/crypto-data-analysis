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

# Directory to save historical trades
output_dir = "data/binance/top_10_historical_trades/"
os.makedirs(output_dir, exist_ok=True)

# Fetch and save historical trades
for symbol in top_10_usdt_pairs:
    print(f"Fetching historical trades for {symbol}...")
    trades = client.get_recent_trades(symbol=symbol, limit=1000)

    output_file = os.path.join(output_dir, f"{symbol}_historical_trades.csv")
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Trade ID", "Price", "Quantity", "Time"])
        for trade in trades:
            writer.writerow([trade['id'], trade['price'], trade['qty'], trade['time']])
    print(f"Saved historical trades for {symbol} to {output_file}")
