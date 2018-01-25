import requests

def load_referencedata():

    url = 'https://api.iextrading.com/1.0/ref-data/symbols'
    stk = requests.get(url)
    return stk.json()

def load_compaydata(ticker):
    url = 'https://api.iextrading.com/1.0/stock/{0}/company'.format(ticker)
    stk = requests.get(url)
    return stk.json()
