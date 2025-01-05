from binance.client import Client
import csv
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

# Fetch and save fees for the top 10 pairs
fees = []
for symbol in top_10_usdt_pairs:
    try:
        trade_fee = client.get_trade_fee(symbol=symbol)
        maker_fee = trade_fee[0]['makerCommission']
        taker_fee = trade_fee[0]['takerCommission']
        fees.append({"Symbol": symbol, "Maker Fee": maker_fee, "Taker Fee": taker_fee})
    except Exception as e:
        print(f"Error fetching fees for {symbol}: {e}")

# Save fees to a CSV
output_file = "data/binance/top_10_fees.csv"
with open(output_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["Symbol", "Maker Fee", "Taker Fee"])
    writer.writeheader()
    writer.writerows(fees)

print(f"Saved fees for top 10 pairs to {output_file}")
