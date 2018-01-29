import marketindex.wikihelper as wiki
# from marketindex.wikihelper import WikiPages
from marketindex import MarketIndices
from marketindex import datahubhelper

"""
class MarketIndices(object):
    
    SP500 = None
    TSX60 = None
    NASDAQ100 = None

    SP500.name = 'S&P 500'
    SP500.url = 'List_of_S%26P_500_companies'
    SP500.cachefilename = 'SP500'

    SP500.name = 'TSX 60'
    SP500.url = 'S%26P/TSX_60'
    SP500.cachefilename = 'TSX60'

    NASDAQ100.name = 'NASDAQ 100'
    NASDAQ100.url = ''
    NASDQA100.cachefilename = 'NASDAQ100'
"""


def load_sp500_from_wiki():
    page = wiki.get_wikihtml(MarketIndices.SP500)
    data = wiki.grab_indexfromhtml(page, MarketIndices.SP500)
    return data


def load_sp500_from_datahub():
    data = datahubhelper.get_sp500_constituent()
    return data

def load_tsx60():
    page = wiki.get_wikihtml(MarketIndices.TSX60)
    data = wiki.grab_indexfromhtml(page, MarketIndices.TSX60)
    return data

def load_dow30():
    page = wiki.get_wikihtml(MarketIndices.DOW30)
    data = wiki.grab_indexfromhtml(page, MarketIndices.DOW30)
    return data

def load_nasdaq100():
    page = wiki.get_wikihtml(MarketIndices.NASDAQ100)
    data = wiki.grab_nasdaq_fromhtml(page, MarketIndices.NASDAQ100)
    return data

def load_indexsymbol(idx):
    switcher = {
        MarketIndices.SP500.name : load_sp500_from_wiki,
        MarketIndices.TSX60.name : load_tsx60,
        MarketIndices.DOW30.name : load_dow30,
        MarketIndices.NASDAQ100.name : load_nasdaq100
        }
    func = switcher.get(idx.name, lambda:None)
    return func()

def main():
    print ("==> start loading TSX 60 index symbols")
    symb = load_tsx60()
    print(symb)
    print ("==> 60 index symbols loaded")

if (__name__ == '__main__'):
    main()
