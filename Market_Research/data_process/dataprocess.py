import datetime
from crossreference import *
import uihelper
from repository import stockpricerepo as pricerepo
from repository import indicatorrepo as idcrepo
from indicator import bollingerbands as bolling

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



