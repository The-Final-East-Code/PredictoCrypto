from datetime import datetime
from coinbase_advanced_trader.coinbase_client import (
    getProduct,
    getProductTicker,
    getProductCandles,
    getCurrencies
    )

# test = getProductTicker("BTC-USD")
def btc_ticker():
    test = getProductCandles("BTC-USD", 1691622800, 1709942405, 86400)
    # Keys to assign to each value in the original data sets
    keys = ["time", "low", "high", "open", "close", "volume"]
    # Use list comprehension to convert each inner list of values into a dictionary
    formatted_data = [dict(zip(keys, values)) for values in test]

    for item in formatted_data:
        # Convert UNIX timestamp to datetime object and format it as a string
        item['time'] = datetime.utcfromtimestamp(item['time']).strftime('%Y-%m-%d %H:%M:%S')
    
    return formatted_data


def storeCurrencies():
    data = getCurrencies()
    with open('data/currencies.json', 'w') as output_file:
        output_file.writelines(data)

# storeCurrencies()
print(btc_ticker())