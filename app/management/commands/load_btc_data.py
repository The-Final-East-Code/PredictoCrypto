from django.core.management.base import BaseCommand
import pandas as pd
from app.models import Bitcoin

class Command(BaseCommand):
    help = 'Import Bitcoin data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the CSV file containing the Bitcoin data')

    def handle(self, *args, **options):
        file_path = options['file_path']

        # Load the data
        df = pd.read_csv(file_path)

        # Iterate over the DataFrame rows and create Bitcoin objects
        for index, row in df.iterrows():
            Bitcoin.objects.create(
                sno=row['SNo'],
                name=row['Name'],
                symbol=row['Symbol'],
                date=pd.to_datetime(row['Date']),
                high=row['High'],
                low=row['Low'],
                open=row['Open'],
                close=row['Close'],
                volume=row['Volume'],
                marketcap=row['Marketcap']
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully imported Bitcoin data from {file_path}'))
