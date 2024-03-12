import requests
from django.core.management.base import BaseCommand
from app.models import Coin  # Update 'app.models' with the correct path to your models

class Command(BaseCommand):
    help = 'Fetches cryptocurrency data from CoinGecko and updates the database'

    def handle(self, *args, **kwargs):
        url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false'
        response = requests.get(url)
        data = response.json()

        for item in data:
            coin, created = Coin.objects.update_or_create(
                cryptoId=item['id'],  # Assuming 'cryptoId' is used to uniquely identify a coin
                defaults={
                    'name': item['name'],
                    'symbol': item['symbol'].upper(),  # Convert symbol to uppercase
                    'currentPrice': item['current_price'],
                    'marketCap': item['market_cap'],
                    'allTimeHigh': item['high_24h'],
                    'allTimeLow': item['low_24h'],
                    'image': item['image'],
                    # Add other fields here as necessary
                }
            )
            print(f"{'Updated' if not created else 'Created'} coin: {coin.name} ({coin.symbol})")

# This script creates a custom Django management command that you can run from your Django project directory using the `manage.py` script, like so:

# python manage.py fetch_coingecko_data
