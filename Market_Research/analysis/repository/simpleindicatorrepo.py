import datetime
import numpy as np
import pandas as pd

from repobase import DbConnection
import adhoc_process as idcpatch

def load_sma(symbol, period, adhoc_patch=False):

    if(adhoc_patch):
        idcpatch.patch_symbol_sma(symbol, period)

    query =  "select effective_date, sma from `idc.sma` WHERE symbol = '{}'".format(symbol)
    
    with DbConnection() as cnx:
        cur = cnx.cursor()
        cur.execute(query)

        df = pd.DataFrame(cur.fetchall())
        if (not df.emtpy):
            df.columns = cur.column_names
            df.set_index('effective_date', inplace=True)

        cur.close()
        return df


