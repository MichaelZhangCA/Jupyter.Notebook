"""
For some common calculation like EMA
"""

import pandas as pd

""" EMA full process
    Calculate EMA from a given price list, will roll the first SMA
"""
def xema(x, period):

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


""" EMA patching process
    calculate EMA from a given price list and given exists ema list
    in this case, the last given ema will be used for calculating and do NOT need roll the first SMA
"""
def cema(x, e, period):

    # start split the ema column and merge to a new source series
    # find position of the last ema
    last_pos = x.index.get_loc(e.last_valid_index())
    # cur off the previous ema valus as reserv part
    exist_ema = e[:last_pos]   # right side is not included
        
    # merge the last ema with the rest of pirce rows
    merge_price = pd.concat([e[last_pos:last_pos+1], x[last_pos+1:]])
        
    # calculate ema from the first value directly, which supposed to be an EMA value already
    cal_ema = merge_price.ewm(span=period, adjust=False).mean()
    
    # merge the reserved ema values with calculated values
    ema = pd.concat([exist_ema, cal_ema])

    return ema

