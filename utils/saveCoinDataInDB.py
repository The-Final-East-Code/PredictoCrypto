import json
from datetime import datetime
from app.models import Coin

def load_data_into_database(json_file_path, coin_crypto_id):
    # Load the JSON data
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Retrieve the Coin instance by cryptoId
    coin = Coin.objects.get(cryptoId=coin_crypto_id)
    
    # Prepare the priceHistory data
    price_history_data = []
    
    for entry in data:
        price_history_entry = {
            "date": datetime.strptime(entry["time"], "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d'),
            "low": entry["low"],
            "high": entry["high"],
            "open": entry["open"],
            "close": entry["close"],
            "volume": entry["volume"],
        }
        
        price_history_data.append(price_history_entry)

    # Update the priceHistory field of the Coin instance
    coin.priceHistory = price_history_data  # Assuming the Coin model has a priceHistory JSONB field
    coin.save()

# Usage example:
json_file_path = '../data/btc_candles.json'
coin_crypto_id = 'btc'  # You'll need to adjust this to match an existing Coin record
load_data_into_database(json_file_path, coin_crypto_id)
