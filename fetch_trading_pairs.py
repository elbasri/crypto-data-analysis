from binance.client import Client
import csv
from config import API_KEY, SECRET_KEY

# Initialize Binance Client
client = Client(API_KEY, SECRET_KEY)

# Fetch all trading pairs info
exchange_info = client.get_exchange_info()
usdt_pairs_info = [
    symbol for symbol in exchange_info['symbols'] if symbol['quoteAsset'] == 'USDT'
]

# Define the output CSV file
output_file = "data/binance/usdt_trading_pairs_info.csv"

# Save detailed trading pair information to a CSV file
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow([
        "Symbol", "Base Asset", "Quote Asset", "Status",
        "Min Price", "Max Price", "Tick Size",
        "Min Qty", "Max Qty", "Step Size",
        "Min Notional"
    ])
    # Write trading pair info
    for pair in usdt_pairs_info:
        filters = {f['filterType']: f for f in pair['filters']}
        writer.writerow([
            pair['symbol'],
            pair['baseAsset'],
            pair['quoteAsset'],
            pair['status'],
            filters.get('PRICE_FILTER', {}).get('minPrice', None),
            filters.get('PRICE_FILTER', {}).get('maxPrice', None),
            filters.get('PRICE_FILTER', {}).get('tickSize', None),
            filters.get('LOT_SIZE', {}).get('minQty', None),
            filters.get('LOT_SIZE', {}).get('maxQty', None),
            filters.get('LOT_SIZE', {}).get('stepSize', None),
            filters.get('MIN_NOTIONAL', {}).get('minNotional', None),
        ])

print(f"Saved detailed info of {len(usdt_pairs_info)} USDT trading pairs to {output_file}")
