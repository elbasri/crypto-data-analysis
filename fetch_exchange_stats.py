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

# Fetch statistics for the top 10 trading pairs
exchange_stats = []

for symbol in top_10_usdt_pairs:
    try:
        ticker = client.get_ticker(symbol=symbol)
        exchange_stats.append({
            "Symbol": symbol,
            "24h Volume": ticker['quoteVolume'],
            "24h High": ticker['highPrice'],
            "24h Low": ticker['lowPrice'],
            "Last Price": ticker['lastPrice'],
            "Price Change (%)": ticker['priceChangePercent']
        })
    except Exception as e:
        print(f"Error fetching statistics for {symbol}: {e}")

# Save the statistics to a CSV
output_file = "data/binance/top_10_exchange_stats.csv"
with open(output_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["Symbol", "24h Volume", "24h High", "24h Low", "Last Price", "Price Change (%)"])
    writer.writeheader()
    writer.writerows(exchange_stats)

print(f"Saved top 10 exchange statistics to {output_file}")
