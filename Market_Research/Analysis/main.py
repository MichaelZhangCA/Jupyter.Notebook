from crossreference import *

from Analysis import show_stockchart
from repobase import DbConnection

serverName = "127.0.0.1"
userName = 'michael'
password = 'Password2017'
databaseName = 'stock_market'

def main():
    # set database connection info
    DbConnection.init_connection(serverName, databaseName, userName, password)
    
    show_stockchart()

if (__name__ == '__main__'):
    main()
