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
    print("Processing Bolling Bands")
    # dataprocess.process_bollingerbands()
    print("process bolling bands done")

    print("Processing Keltner Channels")
    #dataprocess.process_keltnerchannels()
    print("process bolling bands done")

    print("Processing EMA - 20 for Keltner Channels, 12, 26, 9 for MACD")
    dataprocess.process_ema(20)
    dataprocess.process_ema(12)
    dataprocess.process_ema(26)
    dataprocess.process_ema(9)
    print("process EMA done")

if (__name__ == '__main__'):
    main()
