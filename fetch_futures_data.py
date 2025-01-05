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

# Fetch funding rates and open interest
futures_data = []
for symbol in top_10_usdt_pairs:
    try:
        funding_rate = client.futures_funding_rate(symbol=symbol, limit=1)[-1]
        open_interest = client.futures_open_interest(symbol=symbol)
        futures_data.append({
            "Symbol": symbol,
            "Funding Rate": funding_rate['fundingRate'],
            "Open Interest": open_interest['openInterest']
        })
    except Exception as e:
        print(f"Error fetching futures data for {symbol}: {e}")

# Save to CSV
output_file = "data/binance/top_10_futures_data.csv"
with open(output_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["Symbol", "Funding Rate", "Open Interest"])
    writer.writeheader()
    writer.writerows(futures_data)

print(f"Saved futures data for top 10 pairs to {output_file}")