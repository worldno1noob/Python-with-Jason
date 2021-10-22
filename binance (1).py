"""
Module for making HTTP requests to Binance
Attribution: https://github.com/binance/binance-signature-examples/tree/master/python
"""

import hmac
import time
import hashlib
import requests
from urllib.parse import urlencode
import pprint

KEY = '35fd0aa85cb2c172ad1c7b4ac7a72ec24e52f99361d94e8bdd71e3db9296a397'  # Your API Key
# Your Secret Key
SECRET = 'd01e3bb748e74cedb1aee70bc9087b38385eef39af704c885707a8caf0540a49'
# BASE_URL = 'https://api.binance.com' # production base url
BASE_URL = 'https://testnet.binancefuture.com'  # testnet base url

payload = {
    "symbol": "BTCUSDT",
    "side": "SELL",
    "type": "LIMIT",
    "timeInForce": "GTC",
    "quantity": "1",
    "price": "0.2",
    "recvWindow": "5000"
}


def hashing(query_string):
    return hmac.new(SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()


def get_timestamp():
    return int(time.time() * 1000)


def dispatch_request(http_method):
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json;charset=utf-8',
        'X-MBX-APIKEY': KEY
    })
    return {
        'GET': session.get,
        'DELETE': session.delete,
        'PUT': session.put,
        'POST': session.post,
    }.get(http_method, 'GET')

# used for sending request requires the signature


def send_signed_request(http_method, url_path, payload={}):
    query_string = urlencode(payload, True)

    if query_string:
        query_string = "{}&timestamp={}".format(query_string, get_timestamp())
    else:
        query_string = 'timestamp={}'.format(get_timestamp())

    url = BASE_URL + url_path + '?' + query_string + \
        '&signature=' + hashing(query_string)
    print("{} {}".format(http_method, url))
    params = {'url': url, 'params': {}}
    print()
    response = dispatch_request(http_method)(**params)
    return response.json()

# used for sending public data request


def send_public_request(url_path, payload={}):
    query_string = urlencode(payload, True)
    url = BASE_URL + url_path
    if query_string:
        url = url + '?' + query_string
    print("{}".format(url))
    response = dispatch_request('GET')(url=url)
    return response.json()


def get_price(symbol):
    temp = send_public_request('/fapi/v1/ticker/price')
    for i in temp:
        if i["symbol"] == symbol:
            return i["price"]


payload['price'] = get_price("BTCUSDT")

payload['quantity'] = 0.5

payload['side'] = 'SELL'

print(send_signed_request("POST", "/fapi/v1/order", payload))
