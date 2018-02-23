import traceback
from crossreference import *
from repobase import DbConnection
import batch_process as batchprocess

serverName = "127.0.0.1"
userName = 'michael'
password = 'Password2017'
databaseName = 'stock_market'

def set_dbconnection():
    # set database connection info
    DbConnection.init_connection(serverName, databaseName, userName, password)

def main():

    try:
        '''
        print("Processing Bolling Bands")
        # batchprocess.process_bollingerbands()
        print("process bolling bands done")

        print("Processing Keltner Channels")
        #batchprocess.process_keltnerchannels()
        print("process bolling bands done")
        '''

        print("Processing EMA - 20 for Keltner Channels, 12, 26, 9 for MACD, 8/34/55/89/144/233/377 for TTM WAVE ABC")
        batchprocess.process_ema(20)
        batchprocess.process_ema(12)
        batchprocess.process_ema(26)
        batchprocess.process_ema(9)

        
        batchprocess.process_ema(8)
        batchprocess.process_ema(34)
        batchprocess.process_ema(55)
        batchprocess.process_ema(89)
        batchprocess.process_ema(144)
        batchprocess.process_ema(233)
        batchprocess.process_ema(377)
        
        print("process EMA done")

        print("Processing ATR - 14 for Keltner Channels, 10 for comparison")
        batchprocess.process_atr(14)
        batchprocess.process_atr(10)
        print("Process ATR done")


        print("Processing SMA - 20 for Bolling Bands, 150 for moving momentum")
        batchprocess.process_sma(20)
        batchprocess.process_sma(150)
        print("Process SMA done")


        print("Process MACD - 12/26/9")
        #batchprocess.pro
    except:
        print(traceback.format_exc())

if (__name__ == '__main__'):
    main()
