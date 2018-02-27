import datetime
import numpy as np
import pandas as pd

from repobase import DbConnection

"""
# get ajusted price data by symbol and given start date. the result will include start date.
# caller should calculate for the start accurately since it will impact further calculation in some indicators. ex. EMA
# Some indicators like SMA will need load back more than {Period} business days for calculation
"""
def get_stock_adjdata(symbol, startdate):

    query = ("SELECT effective_date, `adj_open`, `adj_high`, `adj_low`, `adj_close`, `adj_volume` FROM `market.stock_price` "
             "WHERE symbol = '{0}' and effective_date >= '{1}' order by effective_date".format(symbol, startdate.strftime('%Y-%m-%d')))

    with DbConnection() as cnx:
        cur = cnx.cursor()

        # reset all valid_flag to 0
        cur.execute(query)

        #df = pd.DataFrame(cur.fetchall(), dtype=np.float)
        df = pd.DataFrame(cur.fetchall())
        df.columns = cur.column_names
        df.set_index('effective_date', inplace=True)

        cur.close()
         
        return df
