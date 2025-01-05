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

# Fetch funding rates
funding_rates = []
for symbol in top_10_usdt_pairs:
    try:
        rate = client.futures_funding_rate(symbol=symbol, limit=1)
        funding_rates.append({
            "Symbol": symbol,
            "Funding Rate": rate[-1]['fundingRate'],
            "Funding Time": rate[-1]['fundingTime']
        })
    except Exception as e:
        print(f"Funding rate unavailable for {symbol}: {e}")

# Save to CSV
output_file = "data/binance/top_10_funding_rates.csv"
with open(output_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["Symbol", "Funding Rate", "Funding Time"])
    writer.writeheader()
    writer.writerows(funding_rates)

print(f"Saved funding rates to {output_file}")
