from requests import Request, Session
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
def apicall23(coin):
    coin= coin.strip()
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=GBP"
    x = requests.get(url)
    a = json.loads(x.text)
    return a[coin.lower()]["gbp"]

def apicall_24_hour_percent(coin):
    coin = coin.lower()
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=gbp&ids={coin}&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=24h"
    x = requests.get(url)
    a = json.loads(x.text)
    b =  a[0]["price_change_percentage_24h_in_currency"]
    z = round(b,3)
    return z
    
#print(apicall_24_hour_percent("bitcoin"))


    
