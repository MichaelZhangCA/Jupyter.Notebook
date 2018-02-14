import datetime
import numpy as np
import pandas as pd

from repobase import DbConnection

def get_bollingerbands_list():
    query = ("SELECT sym.symbol, sym.max_price_date, idc.max_idc_date FROM "
            "(SELECT symbol, MAX(effective_date) AS max_price_date FROM `market.stock_price` GROUP BY symbol) sym "
            "LEFT JOIN "
            "(SELECT symbol, MAX(effective_date) AS max_idc_date FROM `idc.bollinger_bands` GROUP BY symbol) AS idc "
            "ON idc.symbol = sym.symbol")

    with DbConnection() as cnx:
        cur = cnx.cursor(dictionary=True)
        cur.execute(query)
        lst = cur.fetchall()
        cur.close()

        return lst

def __get_insert_sql(symbol):
    ins =("INSERT INTO `stock_market`.`idc.bollinger_bands` (`symbol`, `effective_date`, `adj_close`, `rolling`, `sma20`, `stdev`, `band_upper`, `band_lower`) "
        "VALUES ('{0}','{1}',%(adj_close)s,%(rolling)s,%(sma20)s,%(stdev)s,%(band_upper)s,%(band_lower)s)".format(symbol, '{}'))
    return ins

def refresh_bollingerbands(symbol, idcdata):
    
    if (idcdata.empty):
        return

    # get earliest date in the patch dataset
    firstdate = idcdata.index.min()

    clr = "DELETE FROM `idc.bollinger_bands` WHERE symbol = '{0}' and effective_date >= '{1}'".format(symbol, firstdate.strftime('%Y-%m-%d'))

    ins = __get_insert_sql(symbol)

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

