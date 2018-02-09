import sys
sys.path.append("..\\core")

import iex.IexApi as iexapi
from repository import ReferenceData, IndexRepo, pricerepo
import marketindex
from marketindex import MarketIndices
import quandlwrap
import mysql.connector
import datehelper
from logger import Logger

# service name for logging
service_name = "Market data loading service"

def refresh_symbollist():
    symbolrepo = ReferenceData.SymbolRepo()

    with Logger(service_name) as log:
        log.loginfo ('Load symbol list', '==> start loading symbol list from IEX api')
        symbols = iexapi.load_referencedata()
        log.loginfo ('Load symbol list', ' -> dumped list from IEX')
        symbolrepo.addsymbol(symbols)
        log.loginfo ('Load symbol list', ' -| symbols list updated')

def update_companyinfo():

    with Logger(service_name) as log:

        log.loginfo ('Update company info', '==> start updating symbol company info from IEX api')
        symbolrepo = ReferenceData.SymbolRepo()
        tickers = symbolrepo.get_newtickerlist()
    
        if (len(tickers) > 0):

            log.loginfo ('Update company info', '--> start getting company info for {0} tickers'.format(len(tickers)))
            cmplist = []
            batchcount = 0
            for ticker in tickers:
                cmp = iexapi.load_compaydata(ticker)
                cmplist.append(cmp)
                log.loginfo('Update company info', " -> added company info of : {0}".format(ticker))
    
                batchcount += 1
                # save batch each 100 symbols
                if (batchcount >= 100):

                    log.loginfo ('Update company info', '  : save batched company info')
                    symbolrepo.update_companyinfo(cmplist)
            
                    # reset counter
                    cmplist = []
                    batchcount =0

            # save company info
            if (batchcount>0):
                log.loginfo ('Update company info', ' : save left over records')
                symbolrepo.update_companyinfo(cmplist)
        
            log.loginfo ('Update company info', ' -| all new tickers have been updated')
        else:
            log.loginfo ('Update company info', ' -| there is no new ticker to update')


def batchupdate_marketindices():

    with Logger(service_name) as log:
        log.loginfo('Update Index Constituent', "==> start loading market indices data")

        __update_marketindices(MarketIndices.NASDAQ100)
        __update_marketindices(MarketIndices.SP500)
        __update_marketindices(MarketIndices.DOW30)
        __update_marketindices(MarketIndices.TSX60)

        log.loginfo('Update Index Constituent', " -| market indices data refreshed")

def __update_marketindices(idx):

    with Logger(service_name) as log:
    
        log.loginfo('Update Index Constituent', " -> start loading {0}".format(idx.name))
        data = marketindex.load_indexsymbol(idx)
        IndexRepo.refresh_symbol(idx.name, data)
        log.loginfo('Update Index Constituent', " -> {0} refreshed".format(idx.name))


def dump_symbolhistoricdata():

    with Logger(service_name) as log:
        log.loginfo("Dump Historic Data", "==> start refresh historic data")
        symbols = IndexRepo.get_indexsymbollist()

        for row in symbols:
            # only reload if latest date is no last business day
            tbd1 = datehelper.get_tbd1()

            symbol = row[0]; lastdate = row[1]

            try:
                if (lastdate is None):
                    # new symbol, download full history and dump to table
                    log.loginfo("Dump Historic Data", "--> start dump historic data from quandl for : {}".format(symbol))
                    his = quandlwrap.load_historicdata(symbol)
                    log.loginfo("Dump Historic Data", " -> dump full historic data from quandl for : {}".format(symbol))
                    pricerepo.refresh_symbolhistoric(symbol, his)
                    log.loginfo("Dump Historic Data", " -| Completed historic data dump to database for : {}".format(symbol))
                elif (lastdate < tbd1):
                    log.loginfo("Dump Historic Data", "--> start dump historic data from quandl for : {}".format(symbol))
                    partialhis = quandlwrap.load_partialhistoricdata(symbol, datehelper.get_nextday(lastdate))
                    log.loginfo("Dump Historic Data", " -> dump partial historic data from quandl for : {}".format(symbol))
                    pricerepo.patch_symbolhistoric(symbol, partialhis)
                    log.loginfo("Dump Historic Data", " -| Completed patch missing history for : {}".format(symbol))
                else:
                    # if symbol already up-to-date then skip
                    pass

            except mysql.connector.errors.DataError as err:
                log.logerror("Dump Historic Data", repr("  ! MySQL error : {0}".format(err.msg)))

            except:
                log.logerror("Dump Historic Data", repr("  ! Got error when dumping : {0}, error : {1}".format(symbol, sys.exc_info()[0])))

            print('.', end='', flush=True)

def main():
    # set database connection info
    # DbConnection.init_connection(serverName, databaseName, userName, password)
    
    # update the symbol list with latest data
     refresh_symbollist()
    # patch all new symbol's company data
    # update_companyinfo()

    # update market indicies
    # batchupdate_marketindices()
    # __update_marketindices(MarketIndices.SP500)

    # load index live symbol list
    # dump_symbolhistoricdata()

if (__name__ == '__main__'):
    main()
