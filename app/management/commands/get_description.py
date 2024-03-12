from django.core.management.base import BaseCommand
import requests
from app.models import Coin

class Command(BaseCommand):
    help = 'Fetches and updates cryptocurrency descriptions from CoinGecko'

    def handle(self, *args, **options):
        markets_url = 'https://api.coingecko.com/api/v3/coins/markets'
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 100,
            'page': 1,
            'sparkline': False,
        }

        response = requests.get(markets_url, params=params)
        cryptocurrencies = response.json()

        for crypto in cryptocurrencies:
            try:
                coin = Coin.objects.get(symbol__iexact=crypto['symbol'])
            except Coin.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Symbol not found in database: {crypto['symbol']}"))
                continue

            coin_url = f'https://api.coingecko.com/api/v3/coins/{crypto["id"]}'
            coin_response = requests.get(coin_url)
            coin_info = coin_response.json()

            description = coin_info.get('description', {}).get('en')
            if description:
                description = description.strip()
                if description:
                    coin.description = description
                    coin.save()
                    self.stdout.write(self.style.SUCCESS(f"Updated {crypto['name']} (Symbol: {crypto['symbol'].upper()}) with new description."))
                else:
                    self.stdout.write(self.style.NOTICE(f"No description available for {crypto['name']} (Symbol: {crypto['symbol'].upper()}), skipping."))
            else:
                self.stdout.write(self.style.NOTICE(f"No description available for {crypto['name']} (Symbol: {crypto['symbol'].upper()}), skipping."))
