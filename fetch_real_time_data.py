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

# Fetch real-time market data
real_time_data = []
tickers = client.get_ticker()
for ticker in tickers:
    if ticker['symbol'] in top_10_usdt_pairs:
        real_time_data.append({
            "Symbol": ticker['symbol'],
            "Last Price": ticker['lastPrice'],
            "24h High": ticker['highPrice'],
            "24h Low": ticker['lowPrice'],
            "24h Volume": ticker['quoteVolume'],
        })

# Save to CSV
output_file = "data/binance/top_10_real_time.csv"
with open(output_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["Symbol", "Last Price", "24h High", "24h Low", "24h Volume"])
    writer.writeheader()
    writer.writerows(real_time_data)

print(f"Saved real-time data to {output_file}")
