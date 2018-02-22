import traceback
from crossreference import *
from repobase import DbConnection
import batch_process as idcprocess

serverName = "127.0.0.1"
userName = 'michael'
password = 'Password2017'
databaseName = 'stock_market'

def set_dbconnection():
    # set database connection info
    DbConnection.init_connection(serverName, databaseName, userName, password)

def main():

    try:

        print("Processing Bolling Bands")
        # idcprocess.process_bollingerbands()
        print("process bolling bands done")

        print("Processing Keltner Channels")
        #idcprocess.process_keltnerchannels()
        print("process bolling bands done")

        print("Processing EMA - 20 for Keltner Channels, 12, 26, 9 for MACD, 8/34/55/89/144/233/377 for TTM WAVE ABC")
        # idcprocess.process_ema(20)
        # idcprocess.process_ema(12)
        # idcprocess.process_ema(26)
        # idcprocess.process_ema(9)

        """
        idcprocess.process_ema(8)
        idcprocess.process_ema(34)
        idcprocess.process_ema(55)
        idcprocess.process_ema(89)
        idcprocess.process_ema(144)
        idcprocess.process_ema(233)
        idcprocess.process_ema(377)
        """
        print("process EMA done")

        print("Processing ATR - 14 for Keltner Channels, 10 for comparison")
        idcprocess.process_atr(14)
        idcprocess.process_atr(10)
        print("Process ATR done")


        print("Processing SMA - 20 for Bolling Bands, 150 for moving momentum")
        idcprocess.process_sma(20)
        idcprocess.process_sma(150)
        print("Process SMA done")

    except:
        print(traceback.format_exc())

if (__name__ == '__main__'):
    main()
