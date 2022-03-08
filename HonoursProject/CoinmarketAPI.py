from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json



#print(data)

def searchPercent(coin):
    data = callAPI()
    for i in data:
        if i["symbol"] == coin:
            return i["quote"]["GBP"]["volume_24h"]


     

def search(coin):
    data = callAPI()
    for i in data:
        if i["symbol"] == coin:
            return i["quote"]["GBP"]["price"]

       


def callAPI():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start':'1',
        'limit':'100',
        'convert':'GBP'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'b2246584-2198-44bf-890d-094be5f7a79f',
    }

    session = Session()
    session.headers.update(headers)


    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    return data["data"]


