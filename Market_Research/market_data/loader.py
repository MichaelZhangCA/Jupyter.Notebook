import iex.IexApi as iexapi
from repository import RepoBase, ReferenceData, IndexRepo
import marketindex
from marketindex import MarketIndices



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


def main():
    # set database connection info
    #RepoBase.DbConnection.init_connection(serverName, databaseName, userName, password)
    
    # update the symbol list with latest data
    # refresh_symbollist()
    # patch all new symbol's company data
    # update_companyinfo()

    # update market indicies
    batchupdate_marketindices()

if (__name__ == '__main__'):
    main()
