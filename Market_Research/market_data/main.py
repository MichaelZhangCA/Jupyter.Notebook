from loader import refresh_symbollist, update_companyinfo, batchupdate_marketindices, dump_symbolhistoricdata
# from repository.RepoBase import *

import sys
sys.path.append("..\\core")
from repobase import DbConnection

serverName = "127.0.0.1"
userName = 'michael'
password = 'Password2017'
databaseName = 'stock_market'

def main():
    # set database connection info
    DbConnection.init_connection(serverName, databaseName, userName, password)
    
    # update the symbol list with latest data
    refresh_symbollist()
    print("Symbol list updated")
    
    # patch all new symbol's company data
    update_companyinfo()
    print("Company info updated")

    # update market indicies
    batchupdate_marketindices()
    print("Index constituent updated")

    # load index live symbol list
    dump_symbolhistoricdata()
    print("")
    print("History data updated")

if (__name__ == '__main__'):
    main()
