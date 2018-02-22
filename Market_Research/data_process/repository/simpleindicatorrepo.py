import datetime
import numpy as np
import pandas as pd

from repobase import DbConnection

""" Simple Moving Averages
"""

# check if exists SMA by given symbol and period
def exists_sma(symbol, period):
    query = "SELECT COUNT(1) FROM `idc.sma` WHERE symbol='{}' and period={}".format(symbol, period)
    with DbConnection() as cnx:
        cur = cnx.cursor()
        cur.execute(query)
        cnt = cur.fetchall()[0][0]
        cur.close()

        return cnt != 0

def get_sma_list(period):
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

    ins = "INSERT INTO `stock_market`.`idc.sma` (`symbol`, `effective_date`, `adj_close`, `period`, `sma`, `stdev`) \
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


""" Exponential Moving Averages
"""

def exists_ema(symbol, period):
    query = "SELECT COUNT(1) FROM `idc.ema` WHERE symbol='{}' and period={}".format(symbol, period)
    with DbConnection() as cnx:
        cur = cnx.cursor()
        cur.execute(query)
        cnt = cur.fetchall()[0][0]
        cur.close()

        return cnt != 0

def get_ema_list(period):
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

    ins = "INSERT INTO `stock_market`.`idc.ema` (`symbol`, `effective_date`, `adj_close`, `period`, `ema`) \
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


""" Average True Moving
"""

def exists_atr(symbol, period):
    query = "SELECT COUNT(1) FROM `idc.atr` WHERE symbol='{}' and period={}".format(symbol, period)
    with DbConnection() as cnx:
        cur = cnx.cursor()
        cur.execute(query)
        cnt = cur.fetchall()[0][0]
        cur.close()

        return cnt != 0

def get_atr_list(period):
    query = ("SELECT sym.symbol, sym.max_price_date, idc.max_idc_date FROM "
            "(SELECT symbol, MAX(effective_date) AS max_price_date FROM `market.stock_price` where GROUP BY symbol) sym "
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

    ins = "INSERT INTO `stock_market`.`idc.atr` (`symbol`, `effective_date`,  `adj_high`, `adj_low`, `adj_close`, `tr`, `period`, `atr`) \
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