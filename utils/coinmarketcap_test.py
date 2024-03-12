from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

# url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
# parameters = {
#   'start':'1',
#   'limit':'5000',
#   'convert':'USD'
# }
# url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
# parameters = {
#   'symbol':'BTC',
#   'convert':'USD'
# }
# url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
# parameters = {
#   'symbol':'BTC'
# }
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
parameters = {
  'sort':'cmc_rank',
  'limit':'1000'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '45431fdd-76c4-4786-866e-33983b10d515',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)