import json
import requests
from datetime import datetime
from django.core.management.base import BaseCommand
from app.models import Coin  # Make sure this import points to the correct location of your Coin model

class Command(BaseCommand):
    help = 'Fetches cryptocurrency data from CoinGecko and updates the database with additional information from a local JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file_path', type=str, help='Path to the local JSON file containing additional cryptocurrency data')

    def handle(self, *args, **kwargs):
        json_file_path = kwargs['json_file_path']
        with open(json_file_path, 'r') as file:
            additional_data = json.load(file)['data']

        url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false'
        response = requests.get(url)
        data = response.json()

        for item in data:
            symbol_upper = item['symbol'].upper()
            description = None
            date_added = None
            
            # Search for the symbol in the additional data
            for symbol, details in additional_data.items():
                if symbol.upper() == symbol_upper:
                    # If description is None or empty, set it to "None"
                    description = details.get('description', 'None') if details.get('description') else "None"
                    date_added_str = details.get('date_added')
                    date_added = datetime.strptime(date_added_str, "%Y-%m-%dT%H:%M:%S.%fZ").date() if date_added_str else None
                    break

            # Ensure the Coin model's description field is set to "None" if it would otherwise be empty or null
            description = description if description else "None"

            coin, created = Coin.objects.update_or_create(
                crypto_id=item['id'],
                defaults={
                    'name': item['name'],
                    'symbol': symbol_upper,
                    'description': description,
                    'date_created': date_added or item.get('date_added'),
                    'current_price': item['current_price'],
                    'market_cap': item['market_cap'],
                    'ath': item['ath'],
                    'atl': item['atl'],
                    'image': item['image']
                }
            )
            print(f"{'Updated' if not created else 'Created'} coin: {coin.name} ({coin.symbol}) with additional data")


# This script creates a custom Django management command that you can run from your Django project directory using the `manage.py` script, like so:

# python manage.py fetch_coingecko_data
