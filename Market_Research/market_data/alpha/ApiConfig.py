"""
config API paramters
"""

apikey = 'S1BJMI0DQNCAXEAO'
apibaseurl = 'https://www.alphavantage.co/query?'

apipar = {'function':'', 'symbol':'', 'outputsize':'compact', 'apikey':''}

def __init__(self, **kwargs):
    return super().__init__(**kwargs)

def get_fullurl(symbol, func):

    apipar['function'] = func
    apipar['symbol'] = symbol
    apipar['apikey'] = apikey

    url = apibaseurl
    isfirstpara = True
    for key, value in apipar.items():
        url += ("" if isfirstpara else "&") + key + "=" + value
        isfirstpara = False

    return url

class ApiFunctions(object):
    fun_daily_adjusted = 'TIME_SERIES_DAILY_ADJUSTED'
