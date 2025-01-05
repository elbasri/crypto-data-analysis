from binance.client import Client
import csv
from config import API_KEY, SECRET_KEY

# Initialize Binance Client
client = Client(API_KEY, SECRET_KEY)

# Fetch trading pairs info
exchange_info = client.get_exchange_info()
usdt_pairs_info = {symbol['symbol']: symbol for symbol in exchange_info['symbols'] if symbol['quoteAsset'] == 'USDT'}

# Fetch ticker information (volume and price)
tickers = client.get_ticker()

# Create a dictionary for scoring
usdt_scores = {}

for ticker in tickers:
    if ticker['symbol'] in usdt_pairs_info:
        # Retrieve volume, price, and trading status
        volume = float(ticker['quoteVolume'])  # Quote volume in USDT
        price = float(ticker['lastPrice'])    # Last traded price
        status = usdt_pairs_info[ticker['symbol']]['status']
        
        # Set a weight based on trading status
        status_weight = 1 if status == 'TRADING' else 0.1  # Penalize non-trading pairs

        # Calculate score
        score = (volume * price) * status_weight
        usdt_scores[ticker['symbol']] = {
            "score": score,
            "volume": volume,
            "price": price,
            "status": status,
            **usdt_pairs_info[ticker['symbol']]  # Include all pair-specific data
        }

# Sort by score and select the top 10
top_10_usdt_pairs = sorted(usdt_scores.items(), key=lambda x: x[1]['score'], reverse=True)[:10]

# Save all information for the top 10 pairs to a CSV file
output_file = "data/binance/top_10_usdt_pairs_with_info.csv"
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write header
    writer.writerow([
        "Symbol", "Score", "Volume", "Price", "Status", "Base Asset", "Quote Asset",
        "Min Price", "Max Price", "Tick Size", "Min Qty", "Max Qty", "Step Size", "Min Notional"
    ])
    
    # Write data for each top 10 pair
    for symbol, data in top_10_usdt_pairs:
        filters = {f['filterType']: f for f in data['filters']}
        writer.writerow([
            symbol,
            data['score'],
            data['volume'],
            data['price'],
            data['status'],
            data['baseAsset'],
            data['quoteAsset'],
            filters.get('PRICE_FILTER', {}).get('minPrice', None),
            filters.get('PRICE_FILTER', {}).get('maxPrice', None),
            filters.get('PRICE_FILTER', {}).get('tickSize', None),
            filters.get('LOT_SIZE', {}).get('minQty', None),
            filters.get('LOT_SIZE', {}).get('maxQty', None),
            filters.get('LOT_SIZE', {}).get('stepSize', None),
            filters.get('MIN_NOTIONAL', {}).get('minNotional', None),
        ])

print(f"Saved top 10 USDT pairs with detailed info to {output_file}")
