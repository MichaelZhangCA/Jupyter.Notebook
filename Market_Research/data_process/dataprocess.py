import datetime
from crossreference import *
import uihelper
from repository import stockpricerepo as pricerepo
from repository import indicatorrepo as idcrepo, simpleindicatorrepo as simpleidcrepo
from indicator import bollingerbands as bolling, keltnerchannels as keltner, simpleindicator as simpleidc

from logger import Logger

service_name = "Data Processing Service"
log = Logger(service_name)

def process_bollingerbands():

    log.loginfo("Process Bolling Bands", "==> Start processing Bolling Bands")

    # grab all symbol list from stock price table, with latest Bolling Bands date
    idclist = idcrepo.get_bollingerbands_list()
    symcount = len(idclist)
    curcount = 0

    for idc in idclist:

        symbol = idc['symbol']
        max_price_date = idc['max_price_date']
        max_idc_date = idc['max_idc_date']

        # if there is no bolling bands calculated, start from the beginning
        lastdate = max_price_date
        if (max_idc_date is None):
            lastdate = datetime.date(1901, 1 ,1)
        elif (max_idc_date < max_price_date):
            lastdate = max_idc_date

        if (lastdate != max_price_date):
            log.loginfo("Process Bolling Bands", " -> Start calculating Bolling Bands for : {} from : {}".format(symbol, lastdate.strftime('%Y-%m-%d')))
            # grab stock price
            dfclose = pricerepo.get_stock_adjdata(symbol, lastdate)
            # process
            df = bolling.process_bollingerbands(dfclose)
            # save
            idcrepo.refresh_bollingerbands(symbol, df.dropna())

            log.loginfo("Process Bolling Bands", " -| Complete calculating Bolling Bands for : {}".format(symbol))

        curcount += 1
        uihelper.print_progress(curcount, symcount)

    log.loginfo("Process Bolling Bands", " =| Complete processing Bolling Bands")


def process_keltnerchannels():

    log.loginfo("Process Keltner Channels", "==> Start processing Keltner Channels")

    # grab all symbol list from stock price table, with latest Keltner Channels date
    idclist = idcrepo.get_keltnerchannels_list()
    symcount = len(idclist)
    curcount = 0

    for idc in idclist:

        symbol = idc['symbol']
        max_price_date = idc['max_price_date']
        max_idc_date = idc['max_idc_date']

        # if there is no bolling bands calculated, start from the beginning
        lastdate = max_price_date
        if (max_idc_date is None):
            lastdate = datetime.date(1901, 1 ,1)
        elif (max_idc_date < max_price_date):
            lastdate = max_idc_date

        if (lastdate != max_price_date):
            log.loginfo("Process Keltner Channels", " -> Start calculating Keltner Channels for : {} from : {}".format(symbol, lastdate.strftime('%Y-%m-%d')))
            # grab stock price
            dfclose = pricerepo.get_stock_adjdata(symbol, lastdate)
            # process
            df = keltner.process_keltnerchannels(dfclose)
            # save
            idcrepo.refresh_keltnerchannels(symbol, df.dropna())

            log.loginfo("Process Keltner Channels", " -| Complete Keltner Channels Bands for : {}".format(symbol))

        curcount += 1
        uihelper.print_progress(curcount, symcount)

    log.loginfo("Process Keltner Channels", " =| Complete processing Keltner Channels")


""" Process EMA for all stocks
"""

def process_ema(period):

    log.loginfo("Process EMA", "==> Start processing {} days EMA".format(period))

    # grab all symbol list from stock price table, with latest Keltner Channels date
    idclist = simpleidcrepo.get_ema_list(period)
    symcount = len(idclist)
    curcount = 0

    for idc in idclist:

        symbol = idc['symbol']
        max_price_date = idc['max_price_date']
        max_idc_date = idc['max_idc_date']

        # if there is no bolling bands calculated, start from the beginning
        lastdate = max_price_date
        if (max_idc_date is None):
            lastdate = datetime.date(1901, 1 ,1)
        elif (max_idc_date < max_price_date):
            lastdate = max_idc_date

        if (lastdate != max_price_date):
            log.loginfo("Process EMA", " -> Start calculating {} days EMA for : {} from : {}".format(period, symbol, lastdate.strftime('%Y-%m-%d')))
            # grab stock price
            dfclose = pricerepo.get_stock_adjdata(symbol, lastdate)
            # process
            df = simpleidc.process_ema(dfclose, period)
            # save
            simpleidcrepo.refresh_ema(symbol, period, df.dropna())

            log.loginfo("Process EMA", " -| Complete {} days EMA for : {}".format(period, symbol))

        curcount += 1
        uihelper.print_progress(curcount, symcount)

    log.loginfo("Process EMA", " =| Complete processing {} days EMA".format(period))

