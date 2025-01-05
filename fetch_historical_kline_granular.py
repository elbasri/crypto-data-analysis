from binance.client import Client
from datetime import datetime, timedelta
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

# Parameters for historical data
intervals = [Client.KLINE_INTERVAL_1MINUTE, Client.KLINE_INTERVAL_1HOUR, Client.KLINE_INTERVAL_4HOUR]
end_time = datetime.now()
start_time = end_time - timedelta(days=365)

# Directory to save data
output_dir = "data/binance/top_10_kline_granular/"
os.makedirs(output_dir, exist_ok=True)

# Fetch and save kline data
for symbol in top_10_usdt_pairs:
    for interval in intervals:
        print(f"Fetching {interval} kline data for {symbol}...")
        try:
            klines = client.get_historical_klines(
                symbol,
                interval,
                str(int(start_time.timestamp() * 1000)),
                str(int(end_time.timestamp() * 1000))
            )
            interval_name = interval.split("_")[-1].lower()  # e.g., "1minute" -> "minute"
            output_file = os.path.join(output_dir, f"{symbol}_{interval_name}_kline.csv")
            with open(output_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "Open", "High", "Low", "Close", "Volume"])
                for kline in klines:
                    writer.writerow([kline[0], kline[1], kline[2], kline[3], kline[4], kline[5]])
            print(f"Saved {interval} kline data for {symbol} to {output_file}")
        except Exception as e:
            print(f"Error fetching {interval} kline data for {symbol}: {e}")
