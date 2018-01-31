import requests
import alpha.ApiConfig as cfg
from alpha.ApiConfig import ApiFunctions


def load_daily_adjusted(symbol):

    url = cfg.get_fullurl(symbol, ApiFunctions.fun_daily_adjusted)
    print(url)
    # stk = requests.get(url)
    #return stk.json()

load_daily_adjusted('aapl')
