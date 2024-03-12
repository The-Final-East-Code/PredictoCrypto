# Python version
FROM python:3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy project
COPY . /code/
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
# RUN python manage.py fetch_coingecko_data coinmarketcap-btc-info.json
# RUN python manage.py get_description