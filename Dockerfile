# Python version
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libfreetype6-dev \
    libpng-dev \
    libjpeg-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /code/
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

# RUN python3 manage.py load_btc_data bitcoin.csv
# RUN python manage.py fetch_coingecko_data coinmarketcap-btc-info.json
# RUN python manage.py get_description