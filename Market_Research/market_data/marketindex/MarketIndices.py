
class MarketIndex(object):

    """
    name = ''
    url = ''
    cachefilename = ''
    columns = {}
    """

    def __init__(self, indexname, url, cachename, col_setting):
        self.name = indexname
        self.url = url
        self.cachefilename = cachename
        self.columns = col_setting

# get rid of cache file name to avoid cacheing too much html/csv file
SP500 = MarketIndex('S&P 500', 'List_of_S%26P_500_companies', '', {'symbol':0, 'compony':1})
TSX60 = MarketIndex('TSX 60', 'S%26P/TSX_60', '', {'symbol':0, 'compony':1})
DOW30 = MarketIndex('DOW 30', 'Dow_Jones_Industrial_Average', '', {'symbol':2, 'compony':0})
NASDAQ100 = MarketIndex('NASDAQ 100', 'NASDAQ-100', '', {})

"""
SP500.name = 'S&P 500'
SP500.url = 'List_of_S%26P_500_companies'
SP500.cachefilename = 'SP500'
SP500.columns['symbol'] = 0
SP500.columns['company'] = 1

TSX60.name = 'TSX 60'
TSX60.url = 'S%26P/TSX_60'
TSX60.cachefilename = 'TSX60'
TSX60.columns['symbol'] = 0
TSX60.columns['company'] = 1

DOW30.name = 'DOW 30'
DOW30.url = 'Dow_Jones_Industrial_Average'
DOW30.cachefilename = 'DOW30'
DOW30.columns['symbol'] = 2
DOW30.columns['company'] = 0

NASDAQ100.name = 'NASDAQ 100'
NASDAQ100.url = 'NASDAQ-100'
NASDAQ100.cachefilename = 'NASDAQ100'
"""
