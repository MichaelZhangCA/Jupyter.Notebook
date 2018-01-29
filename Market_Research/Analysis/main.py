# from loader import refresh_symbollist, update_companyinfo, batchupdate_marketindices, dump_symbolhistoricdata
from repository.repobase import *

serverName = "127.0.0.1"
userName = 'michael'
password = 'Password2017'
databaseName = 'stock_market'

def main():
    # set database connection info
    DbConnection.init_connection(serverName, databaseName, userName, password)
    

if (__name__ == '__main__'):
    main()
