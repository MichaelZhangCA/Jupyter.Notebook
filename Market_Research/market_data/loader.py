import sys
import iex.IexApi as iexapi
from repository import RepoBase, ReferenceData, IndexRepo, pricerepo
import marketindex
from marketindex import MarketIndices
import quandlwrap
import mysql.connector
from utility import datehelper


serverName = "127.0.0.1"
userName = 'michael'
password = 'Password2017'
databaseName = 'stock_market'

def refresh_symbollist():
    symbolrepo = ReferenceData.SymbolRepo()

    print ('==> start loading data from iex api')
    symbols = iexapi.load_referencedata()
    print ('==> start save data to database')

    symbolrepo.addsymbol(symbols)

    print ('==> symbols saved')

def update_companyinfo():

    symbolrepo = ReferenceData.SymbolRepo()

    tickers = symbolrepo.get_newtickerlist()
    
    if (len(tickers) > 0):

        print ('==> start getting company info for {0} tickers'.format(len(tickers)))
        cmplist = []
        batchcount = 0
        for ticker in tickers:
            cmp = iexapi.load_compaydata(ticker)
            cmplist.append(cmp)
            print("  : added company info of '{0}'".format(ticker))
    
            batchcount += 1
            # save batch each 100 symbols
            if (batchcount >= 100):

                print ('==> save the batch info')
                symbolrepo.update_companyinfo(cmplist)
            
                # reset counter
                cmplist = []
                batchcount =0

        # save company info
        if (batchcount>0):
            print ('==> start writting left over records')
            symbolrepo.update_companyinfo(cmplist)
        
        print ('==> all new tickers have been updated')
    else:
        print ('==| there is no new ticker to update')


def batchupdate_marketindices():
    update_marketindices(MarketIndices.NASDAQ100)
    update_marketindices(MarketIndices.SP500)
    update_marketindices(MarketIndices.DOW30)
    update_marketindices(MarketIndices.TSX60)

def update_marketindices(idx):
    
    print("==> start loading {0}".format(idx.name))
    data = marketindex.load_indexsymbol(idx)
    IndexRepo.refresh_symbol(idx.name, data)
    print("==> {0} refreshed".format(idx.name))


def dump_symbolhistoricdata():
    symbols = IndexRepo.get_indexsymbollist()

    for row in symbols:
        # only reload if latest date is no last business day
        tbd1 = datehelper.get_tbd1()

        symbol = row[0]; lastdate = row[1]

        try:
            if (lastdate is None):
                # new symbol, download full history and dump to table
                print("==> start dump historic data from quandl for : {}".format(symbol))
                his = quandlwrap.load_historicdata(symbol)
                print(" -> dump full historic data from quandl for : {}".format(symbol))
                pricerepo.refresh_symbolhistoric(symbol, his)
                print(" -> Completed historic data dump to database for : {}".format(symbol))
            elif (lastdate < tbd1):
                print("==> start dump historic data from quandl for : {}".format(symbol))
                partialhis = quandlwrap.load_partialhistoricdata(symbol, datehelper.get_nextday(lastdate))
                print(" -> dump partial historic data from quandl for : {}".format(symbol))
                pricerepo.patch_symbolhistoric(symbol, partialhis)
                print(" -> Completed patch missing history for : {}".format(symbol))
            else:
                # if symbol already up-to-date then skip
                pass

        except mysql.connector.errors.DataError as err:
            print("  ! MySQL error : {0}".format(err.msg))

        except:
            print("  ! Got error when dumping : {0}, error : {1}".format(symbol, sys.exc_info()[0]))

def main():
    # set database connection info
    #RepoBase.DbConnection.init_connection(serverName, databaseName, userName, password)
    
    # update the symbol list with latest data
    # refresh_symbollist()
    # patch all new symbol's company data
    # update_companyinfo()

    # update market indicies
    # batchupdate_marketindices()

    # load index live symbol list
    dump_symbolhistoricdata()

if (__name__ == '__main__'):
    main()
