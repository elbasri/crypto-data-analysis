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

# Directory to save order books
output_dir = "data/binance/top_10_order_books/"
os.makedirs(output_dir, exist_ok=True)

# Fetch and save order book data
for symbol in top_10_usdt_pairs:
    print(f"Fetching order book for {symbol}...")
    depth = client.get_order_book(symbol=symbol, limit=100)

    output_file = os.path.join(output_dir, f"{symbol}_order_book.csv")
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Type", "Price", "Quantity"])
        for bid in depth['bids']:
            writer.writerow(["Bid", bid[0], bid[1]])
        for ask in depth['asks']:
            writer.writerow(["Ask", ask[0], ask[1]])
    print(f"Saved order book for {symbol} to {output_file}")
