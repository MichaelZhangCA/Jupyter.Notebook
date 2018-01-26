import marketindex.wikihelper as wiki
from marketindex.wikihelper import WikiPages

class MarketIndices(object):
    """ define name of major market indices"""

    SP500 = "S&P 500"
    TSX60 = "TSX 60"
    NASDAQ100 = "NASDAQ 100"


def load_sp500():
    page = wiki.get_wikihtml(WikiPages.url_sp500, WikiPages.file_sp500)
    data = wiki.grab_indexfromhtml(page, WikiPages.file_sp500)
    return data

def load_tsx60():
    page = wiki.get_wikihtml(WikiPages.url_tsx60, WikiPages.file_tsx60)
    data = wiki.grab_indexfromhtml(page, WikiPages.file_tsx60)
    return data

def load_indexsymbol(indexname):
    switcher = {
        MarketIndices.SP500 : load_sp500,
        MarketIndices.TSX60 : load_tsx60
        }
    func = switcher.get(indexname, lambda:None)
    return func()

def main():
    print ("==> start loading TSX 60 index symbols")
    symb = load_tsx60()
    print(symb)
    print ("==> 60 index symbols loaded")

if (__name__ == '__main__'):
    main()
