"""
For some common calculation like EMA
"""

import pandas as pd

""" calculate EMA from a given price list, will roll the first SMA
"""
def ream(x, period):

    # find the first non-NaN postion
    first_nn = x.index.get_loc(x.first_valid_index())
    
    # roll the first x days for fist SMA start point, roll for (period + first_nn rows) with windows (period)
    ema_rolling = x[:period + first_nn].rolling(period)

    # combine the first SMA with the rest close adj price
    ema_con = pd.concat([ema_rolling.mean(), x[period + first_nn:]])
    #ema_con.head(30)
    #df['ema_con'] = ema_con
    ema = ema_con.ewm(span=period, adjust=False).mean()

    return ema


""" 
calculate EMA from a given price list, with a given exists ema
in this case, the last given ema will be used for calculating and do NOT need roll the first SMA
"""
def xeam(x, ema, period):

    # find the first non-NaN postion
    first_ema = ema.index.get_loc(ema.last_valid_index())
    
    # roll the first x days for fist SMA start point, roll for (period + first_nn rows) with windows (period)
    ema_rolling = x[:period + first_nn].rolling(period)

    # combine the first SMA with the rest close adj price
    ema_con = pd.concat([ema_rolling.mean(), x[period + first_nn:]])
    #ema_con.head(30)
    #df['ema_con'] = ema_con
    ema = ema_con.ewm(span=period, adjust=False).mean()

    return ema

