import datetime
import numpy as np
import pandas as pd

from repobase import DbConnection

"""
reposotiry for all essential indicators
"""

# ==================================================== ATR - Simple Moving Average ====================================================

""" Simple Moving Averages
"""

# check if exists SMA by given symbol and period
def exists_sma(symbol, period):
    query = "SELECT COUNT(1) FROM `idc.sma` WHERE symbol='{}' and period={} LIMIT 1".format(symbol, period)
    with DbConnection() as cnx:
        cur = cnx.cursor()
        cur.execute(query)
        cnt = cur.fetchall()[0][0]
        cur.close()

        return cnt != 0

def get_sma_lastdate(period):
    query = ("SELECT sym.symbol, sym.max_price_date, idc.max_idc_date FROM "
            "(SELECT symbol, MAX(effective_date) AS max_price_date FROM `market.stock_price` GROUP BY symbol) sym "
            "LEFT JOIN "
            "(SELECT symbol, MAX(effective_date) AS max_idc_date FROM `idc.sma` WHERE `period`={} GROUP BY symbol) AS idc "
            "ON idc.symbol = sym.symbol".format(period))

    with DbConnection() as cnx:
        cur = cnx.cursor(dictionary=True)
        cur.execute(query)
        lst = cur.fetchall()
        cur.close()

        return lst

def refresh_sma(symbol, period, idcdata):
    
    if (idcdata.empty):
        return

    # get earliest date in the patch dataset
    firstdate = idcdata.index.min()

    clr = "DELETE FROM `idc.sma` WHERE symbol='{}' and period={} and effective_date >= '{}'".format(symbol, period, firstdate.strftime('%Y-%m-%d'))

    ins = "INSERT INTO `idc.sma` (`symbol`, `effective_date`, `adj_close`, `period`, `sma`, `stdev`) \
           VALUES ('{0}','{1}', %(adj_close)s, {2}, %(sma)s, %(stdev)s )".format(symbol, '{}', period)

    # cleanse data frame NaN
    idcdata = idcdata.where((pd.notnull(idcdata)), None)

    with DbConnection() as cnx:
        cur = cnx.cursor()

        # clear current record
        cur.execute(clr)
        cnx.commit()

        idcdic = idcdata.to_dict(orient='index')

        # insert from the list
        for date, row in idcdic.items():
            # put effective date to query
            query = ins.format(date.strftime('%Y-%m-%d'))
            cur.execute(query, row)
            
        cnx.commit()
        cur.close()

# ==================================================== ATR - Exponential Moving Average ====================================================

""" Exponential Moving Averages
"""

def exists_ema(symbol, period):
    query = "SELECT COUNT(1) FROM `idc.ema` WHERE symbol='{}' and period={} LIMIT 1".format(symbol, period)
    with DbConnection() as cnx:
        cur = cnx.cursor()
        cur.execute(query)
        cnt = cur.fetchall()[0][0]
        cur.close()

        return cnt != 0

def get_ema_lastdate(period):
    query = ("SELECT sym.symbol, sym.max_price_date, idc.max_idc_date FROM "
            "(SELECT symbol, MAX(effective_date) AS max_price_date FROM `market.stock_price` GROUP BY symbol) sym "
            "LEFT JOIN "
            "(SELECT symbol, MAX(effective_date) AS max_idc_date FROM `idc.ema` WHERE `period`={} GROUP BY symbol) AS idc "
            "ON idc.symbol = sym.symbol".format(period))

    with DbConnection() as cnx:
        cur = cnx.cursor(dictionary=True)
        cur.execute(query)
        lst = cur.fetchall()
        cur.close()

        return lst

def refresh_ema(symbol, period, idcdata):
    
    if (idcdata.empty):
        return

    # get earliest date in the patch dataset
    firstdate = idcdata.index.min()

    clr = "DELETE FROM `idc.ema` WHERE symbol='{}' and period={} and effective_date >= '{}'".format(symbol, period, firstdate.strftime('%Y-%m-%d'))

    ins = "INSERT INTO `idc.ema` (`symbol`, `effective_date`, `adj_close`, `period`, `ema`) \
           VALUES ('{0}','{1}', %(adj_close)s, {2}, %(ema)s )".format(symbol, '{}', period)

    # cleanse data frame NaN
    idcdata = idcdata.where((pd.notnull(idcdata)), None)

    with DbConnection() as cnx:
        cur = cnx.cursor()

        # clear current record
        cur.execute(clr)
        cnx.commit()

        idcdic = idcdata.to_dict(orient='index')

        # insert from the list
        for date, row in idcdic.items():
            # put effective date to query
            query = ins.format(date.strftime('%Y-%m-%d'))
            cur.execute(query, row)
            
        cnx.commit()
        cur.close()


""" return ema for given date, typically used to calclate ema for following days, as a start point
"""
def get_ema_by_date(symbol, period, asofdate):
    query = "SELECT effective_date, ema FROM `idc.ema` WHERE symbol='{}' and period={} and effective_date='{}'".format(symbol, period, asofdate.strftime('%Y-%m-%d'))

    with DbConnection() as cnx:
        cur = cnx.cursor(dictionary=True)
        cur.execute(query)
        lst = cur.fetchall()

        cur.close()
        return lst

# ==================================================== ATR - Average True Range ====================================================

""" Average True Moving
"""

def exists_atr(symbol, period):
    query = "SELECT COUNT(1) FROM `idc.atr` WHERE symbol='{}' and period={} LIMIT 1".format(symbol, period)
    with DbConnection() as cnx:
        cur = cnx.cursor()
        cur.execute(query)
        cnt = cur.fetchall()[0][0]
        cur.close()

        return cnt != 0

def get_atr_lastdate(period):
    query = ("SELECT sym.symbol, sym.max_price_date, idc.max_idc_date FROM "
            "(SELECT symbol, MAX(effective_date) AS max_price_date FROM `market.stock_price` GROUP BY symbol) sym "
            "LEFT JOIN "
            "(SELECT symbol, MAX(effective_date) AS max_idc_date FROM `idc.atr` WHERE `period`={} GROUP BY symbol) AS idc "
            "ON idc.symbol = sym.symbol".format(period))

    with DbConnection() as cnx:
        cur = cnx.cursor(dictionary=True)
        cur.execute(query)
        lst = cur.fetchall()
        cur.close()

        return lst

def refresh_atr(symbol, period, idcdata):
    
    if (idcdata.empty):
        return

    # get earliest date in the patch dataset
    firstdate = idcdata.index.min()

    clr = "DELETE FROM `idc.atr` WHERE symbol='{}' and period={} and effective_date >= '{}'".format(symbol, period, firstdate.strftime('%Y-%m-%d'))

    ins = "INSERT INTO `idc.atr` (`symbol`, `effective_date`,  `adj_high`, `adj_low`, `adj_close`, `tr`, `period`, `atr`) \
           VALUES ('{0}','{1}', %(adj_high)s, %(adj_low)s, %(adj_close)s, %(TR)s, {2}, %(atr)s )".format(symbol, '{}', period)

    # cleanse data frame NaN
    idcdata = idcdata.where((pd.notnull(idcdata)), None)

    with DbConnection() as cnx:
        cur = cnx.cursor()

        # clear current record
        cur.execute(clr)
        cnx.commit()

        idcdic = idcdata.to_dict(orient='index')

        # insert from the list
        for date, row in idcdic.items():
            # put effective date to query
            query = ins.format(date.strftime('%Y-%m-%d'))
            cur.execute(query, row)
            
        cnx.commit()
        cur.close()


""" return atr for given date, typically used to calclate ema for following days, as a start point
"""
def get_ema_by_date(symbol, period, asofdate):
    query = "SELECT effective_date, atr FROM `idc.atr` WHERE symbol='{}' and period={} and effective_date='{}'".format(symbol, period, asofdate.strftime('%Y-%m-%d'))

    with DbConnection() as cnx:
        cur = cnx.cursor(dictionary=True)
        cur.execute(query)
        lst = cur.fetchall()

        cur.close()
        return lst

# ==================================================== MACD - Moving Average Convergence / Divergence ====================================================

""" MACD - Moving Average Convergence / Divergence
"""

def exists_macd(symbol, shortperiod, longperiod, signalperiod):
    query = "SELECT COUNT(1) FROM `idc.macd` WHERE symbol='{}' and short_period={} and long_period={} and signal_period={} LIMIT 1".format(symbol, shortperiod, longperiod, signalperiod)
    with DbConnection() as cnx:
        cur = cnx.cursor()
        cur.execute(query)
        cnt = cur.fetchall()[0][0]
        cur.close()

        return cnt != 0

def get_macd_lastdate(shortperiod, longperiod, signalperiod):
    query = ("SELECT sym.symbol, sym.max_price_date, idc.max_idc_date FROM "
            "(SELECT symbol, MAX(effective_date) AS max_price_date FROM `market.stock_price` GROUP BY symbol) sym "
            "LEFT JOIN "
            "(SELECT symbol, MAX(effective_date) AS max_idc_date FROM `idc.macd` WHERE short_period={} and long_period={} and signal_period={} GROUP BY symbol) AS idc "
            "ON idc.symbol = sym.symbol".format(shortperiod, longperiod, signalperiod))

    with DbConnection() as cnx:
        cur = cnx.cursor(dictionary=True)
        cur.execute(query)
        lst = cur.fetchall()
        cur.close()

        return lst

def refresh_macd(symbol, shortperiod, longperiod, signalperiod, idcdata):
    
    if (idcdata.empty):
        return

    # get earliest date in the patch dataset
    firstdate = idcdata.index.min()

    clr = "DELETE FROM `idc.macd` WHERE symbol='{}' and short_period={} and long_period={} and signal_period={} and effective_date >= '{}'".format(symbol, shortperiod, longperiod, signalperiod, firstdate.strftime('%Y-%m-%d'))

    ins = "INSERT INTO `idc.macd` (`symbol`, `effective_date`, `short_period`, `long_period`, `signal_period`, `short_ema`, `long_ema`, `macd`, `macd_ema`, `macd_histogram`) \
           VALUES ('{}','{}', {}, {}, {}, %(short_ema)s, %(long_ema)s, %(macd)s, %(macd_ema)s, %(macd_histogram)s )".format(symbol, '{}', shortperiod, longperiod, signalperiod)

    # cleanse data frame NaN
    idcdata = idcdata.where((pd.notnull(idcdata)), None)

    with DbConnection() as cnx:
        cur = cnx.cursor()

        # clear current record
        cur.execute(clr)
        cnx.commit()

        idcdic = idcdata.to_dict(orient='index')

        # insert from the list
        for date, row in idcdic.items():
            # put effective date to query
            query = ins.format(date.strftime('%Y-%m-%d'))
            cur.execute(query, row)
            
        cnx.commit()
        cur.close()

def get_macd_by_date(symbol, shortperiod, longperiod, signalperiod, asofdate):
    #query = "SELECT effective_date, atr FROM `idc.atr` WHERE symbol='{}' and period={} and effective_date='{}'".format(symbol, period, asofdate.strftime('%Y-%m-%d'))
    query = "SELECT effective_date, macd, macd_ema, macd_histogram FROM `idc.macd` \
            WHERE symbol='{}' and short_period={} and long_period={} and signal_period={} and effective_date='{}'" \
            .format(symbol, shortperiod, longperiod, signalperiod, asofdate.strftime('%Y-%m-%d'))
    with DbConnection() as cnx:
        cur = cnx.cursor(dictionary=True)
        cur.execute(query)
        lst = cur.fetchall()

        cur.close()
        return lst
