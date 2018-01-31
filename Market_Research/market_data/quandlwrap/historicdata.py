import quandl

def load_historicdata(symbol):
    data = quandl.get("WIKI/{}".format(symbol))

    return data

def load_partialhistoricdata(symbol, startdate):
    data = quandl.get("WIKI/{}".format(symbol), start_date="'{}'".format(startdate.strftime('%Y-%m-%d')))
    return data