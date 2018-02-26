import pandas as pd

def xeam(x, period):

    # find the first non-NaN postion
    first_nn = df.index.get_loc(x.first_valid_index())
    
    # roll the first x days for fist SMA start point, roll for (period + first_nn rows) with windows (period)
    ema_rolling = x[:period + first_nn].rolling(period)

    # combine the first SMA with the rest close adj price
    ema_con = pd.concat([ema_rolling.mean(), x[period + first_nn:]])
    #ema_con.head(30)
    #df['ema_con'] = ema_con
    ema = ema_con.ewm(span=period, adjust=False).mean()

    return ema

