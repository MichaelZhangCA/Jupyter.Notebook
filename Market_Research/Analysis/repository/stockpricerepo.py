import datetime
import numpy as np
import pandas as pd
from repository.repobase import DbConnection

def get_stockprice(symbol):

    query = query = "select * from (SELECT effective_date, `open`, `high`, `low`, `close`, `volume`, `adj_open`, `adj_high`, `adj_low`, `adj_close`, `adj_volume` FROM `market.stock_price` WHERE symbol = '{0}' order by effective_date DESC limit 1000) sub order by effective_date ASC".format(symbol)
    
    with DbConnection() as cnx:
        cur = cnx.cursor()

        # reset all valid_flag to 0
        cur.execute(query)

        df = pd.DataFrame(cur.fetchall(), dtype=np.float)
        df.columns = cur.column_names
        df.set_index('effective_date', inplace=True)

        cur.close()
         
        return df
