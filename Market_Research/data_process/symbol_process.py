from repository import stockpricerepo as pricerepo
from repository import indicatorrepo as idcrepo, simpleindicatorrepo as simpleidcrepo
from indicator import bollingerbands as bolling, keltnerchannels as keltner, simpleindicator as simpleidc

def process_symbol_sma(symbol, period, startdate):
    # grab stock price
    dfclose = pricerepo.get_stock_adjdata(symbol, startdate)
    # process
    df = simpleidc.process_sma(dfclose, period)
    # save
    simpleidcrepo.refresh_sma(symbol, period, df.dropna())


def process_symbol_ema(symbol, period, startdate):
    # grab stock price
    dfclose = pricerepo.get_stock_adjdata(symbol, startdate)
    # process
    df = simpleidc.process_ema(dfclose, period)
    # save
    simpleidcrepo.refresh_ema(symbol, period, df.dropna())


def process_symbol_atr(symbol, period, startdate):
    # grab stock price
    dfclose = pricerepo.get_stock_adjdata(symbol, startdate)
    # process
    df = simpleidc.process_atr(dfclose, period)
    # save
    simpleidcrepo.refresh_atr(symbol, period, df.dropna())
