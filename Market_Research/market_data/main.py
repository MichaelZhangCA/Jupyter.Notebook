from loader import refresh_symbollist, update_companyinfo, batchupdate_marketindices, dump_symbolhistoricdata
from repository.RepoBase import *

serverName = "127.0.0.1"
userName = 'michael'
password = 'Password2017'
databaseName = 'stock_market'

def main():
    # set database connection info
    DbConnection.init_connection(serverName, databaseName, userName, password)
    
    # update the symbol list with latest data
    refresh_symbollist()
    # patch all new symbol's company data
    update_companyinfo()

    # update market indicies
    batchupdate_marketindices()

    # load index live symbol list
    dump_symbolhistoricdata()

if (__name__ == '__main__'):
    main()
