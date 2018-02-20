import datetime
import numpy as np
import pandas as pd

from repobase import DbConnection

""" Exponential Moving Averages
"""

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

    clr = "DELETE FROM `idc.ema` WHERE symbol = '{0}' and period={1} and effective_date >= '{1}'".format(symbol, firstdate.strftime('%Y-%m-%d'), period)

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

