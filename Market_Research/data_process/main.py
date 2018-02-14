from crossreference import *
from repobase import DbConnection
import dataprocess

serverName = "127.0.0.1"
userName = 'michael'
password = 'Password2017'
databaseName = 'stock_market'

def set_dbconnection():
    # set database connection info
    DbConnection.init_connection(serverName, databaseName, userName, password)

def main():
    dataprocess.process_bollingerbands()
    print("process bolling bands done")

if (__name__ == '__main__'):
    main()
