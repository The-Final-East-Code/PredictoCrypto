from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings

class Command(BaseCommand):
    help = 'Create the "coins" database and its tables'

    def handle(self, *args, **options):
        # SQL statement to create tables
        create_tables_sql = """
        -- USERS
        CREATE TABLE IF NOT EXISTS accounts_customuser (
            id SERIAL PRIMARY KEY,
            password VARCHAR(128) NOT NULL,
            last_login TIMESTAMP WITH TIME ZONE,
            is_superuser BOOLEAN NOT NULL,
            username VARCHAR(150) UNIQUE NOT NULL,
            first_name VARCHAR(30) NOT NULL,
            last_name VARCHAR(150) NOT NULL,
            email VARCHAR(254) UNIQUE NOT NULL,
            is_staff BOOLEAN NOT NULL,
            is_active BOOLEAN NOT NULL,
            date_joined TIMESTAMP WITH TIME ZONE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(45) NOT NULL,
            last_name VARCHAR(45) NOT NULL,
            email VARCHAR(50),
            create_date DATE DEFAULT CURRENT_DATE NOT NULL,
            last_update TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );

        -- COINS
        CREATE TABLE IF NOT EXISTS app_coin (
            id SERIAL PRIMARY KEY,
            crypto_id VARCHAR(50) NOT NULL,
            name VARCHAR(50) NOT NULL,
            symbol VARCHAR(50) NOT NULL,
            rank INTEGER,
            market_cap_rank INTEGER,
            description VARCHAR DEFAULT NULL,
            current_price DOUBLE PRECISION NOT NULL,
            market_cap DOUBLE PRECISION,
            ath DOUBLE PRECISION,
            atl DOUBLE PRECISION,
            date_created DATE DEFAULT NULL,
            image VARCHAR(200),
            price_history JSONB
        );

        CREATE TABLE IF NOT EXISTS bitcoin (
            sno INTEGER PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            symbol VARCHAR(10) NOT NULL,
            date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            high NUMERIC(19, 4) NOT NULL,
            low NUMERIC(19, 4) NOT NULL,
            open NUMERIC(19, 4) NOT NULL,
            close NUMERIC(19, 4) NOT NULL,
            volume NUMERIC(19, 4) NOT NULL,
            market_cap NUMERIC(19, 4) NOT NULL
        );

        -- PlotImages
        CREATE TABLE IF NOT EXISTS plot_images (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES accounts_customuser(id) ON DELETE CASCADE,
            path VARCHAR(256) NOT NULL,
            description TEXT,
            date_created TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            coin_id INTEGER REFERENCES app_coin(id) ON DELETE SET NULL
        );

        -- CsvUploads
        CREATE TABLE IF NOT EXISTS csv_uploads (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES accounts_customuser(id) ON DELETE CASCADE,
            path VARCHAR(256) NOT NULL,
            description TEXT,
            date_created TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            coin_id INTEGER REFERENCES app_coin(id) ON DELETE SET NULL
        );

        -- GptResponses
        CREATE TABLE IF NOT EXISTS gpt_responses (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES accounts_customuser(id) ON DELETE CASCADE,
            path VARCHAR(256) NOT NULL,
            description TEXT,
            date_created TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            coin_id INTEGER REFERENCES app_coin(id) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS platform (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            symbol VARCHAR(10) NOT NULL,
            slug VARCHAR(50) NOT NULL,
            token_address VARCHAR(100) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS cryptodata (
            id SERIAL PRIMARY KEY,
            crypto_id INTEGER UNIQUE NOT NULL,
            rank INTEGER NOT NULL,
            name VARCHAR(50) NOT NULL,
            symbol VARCHAR(10) NOT NULL,
            slug VARCHAR(50) NOT NULL,
            is_active BOOLEAN NOT NULL,
            first_historical_data TIMESTAMP WITH TIME ZONE NOT NULL,
            last_historical_data TIMESTAMP WITH TIME ZONE NOT NULL,
            platform_id INTEGER REFERENCES platform(id)
        );

        ALTER TABLE accounts_customuser ADD COLUMN bio TEXT;
        ALTER TABLE accounts_customuser ADD COLUMN profile_picture VARCHAR(255);
        """

        with connection.cursor() as cursor:
            cursor.execute(create_tables_sql)
            self.stdout.write(self.style.SUCCESS("Tables created successfully."))

