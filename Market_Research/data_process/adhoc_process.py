import datetime

from crossreference import *
import uihelper, appvariable
from logger import Logger

from repository import simpleindicatorrepo as simpleidcrepo
import symbol_process as symproc

service_name = "Data Processing Service"
log = Logger(service_name)

""" patch SMA for given symbol & period
"""
def patch_symbol_sma(symbol, period):
    if(not simpleidcrepo.exists_sma(symbol, period)):
        log.loginfo("Patch SMA", "--> Start patching {} days SMA for : {}".format(period, symbol))
        symproc.process_symbol_sma(symbol, period, appvariable.STOCK_START_DATE)
        log.loginfo("Patch SMA", "--| Completed patching {} days SMA for : {}".format(period, symbol))
    

""" patch EMA for given symbol & period
"""
def patch_symbol_ema(symbol, period):
    if(not simpleidcrepo.exists_ema(symbol, period)):
        log.loginfo("Patch EMA", "--> Start patching {} days EMA for : {}".format(period, symbol))
        symproc.process_symbol_ema(symbol, period, appvariable.STOCK_START_DATE)
        log.loginfo("Patch EMA", "--| Completed patching {} days EMA for : {}".format(period, symbol))


""" patch ATR for given symbol & period
"""
def patch_symbol_atr(symbol, period):
    if(not simpleidcrepo.exists_atr(symbol, period)):
        log.loginfo("Patch ATR", "--> Start patching {} days ATR for : {}".format(period, symbol))
        symproc.process_symbol_atr(symbol, period, appvariable.STOCK_START_DATE)
        log.loginfo("Patch ATR", "--| Completed patching {} days ATR for : {}".format(period, symbol))


""" patch MACD for given symbol & periods
"""
def patch_symbol_macd(symbol, shortperiod, longperiod, signalperiod):
    if(not simpleidcrepo.exists_macd(symbol, shortperiod, longperiod, signalperiod)):
        log.loginfo("Patch MACD", "--> Start patching {}/{}/{} days MACD for : {}".format(shortperiod, longperiod, signalperiod, symbol))
        symproc.process_symbol_macd(symbol, shortperiod, longperiod, signalperiod)
        log.loginfo("Patch ATR", "--| Completed patching {}/{}/{} days ATR for : {}".format(shortperiod, longperiod, signalperiod, symbol))
