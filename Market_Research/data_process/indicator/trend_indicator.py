"""
Trend indicators measure the direction and strength of a trend
using some form of price averageing to establish a baseline

Typical treand indicator includes:
  - SMA / EMA
  - MACD
  - Parabolic SAR
"""
import pandas as pd
import commonalgorithm as comalgo


# process SMA / Deviation for x days
def process_sma(df, period):
    
    # get rolling list
    rolling = df["adj_close"].rolling(period)

    # construct return DF
    df['sma'] = rolling.mean()
    # by default, ddof is 1 which calculate sample deviation
    df['stdev'] = rolling.std(ddof=0)
    df['smpldev'] = rolling.std(ddof=1)

    return df


# process EMA for x days
def process_ema(df, period):
    
    """ ema logic moved to common algorithm
    # roll the first x days for fist SMA start point
    ema_rolling = df[:period]["adj_close"].rolling(period)

    # combine the first SMA with the rest close adj price
    ema_con = pd.concat([ema_rolling.mean(), df[period:]['adj_close']])
    #con.head(30)
    #df['ema_con'] = ema_con
    df['ema'] = ema_con.ewm(span=period, adjust=False).mean()
    """

    df['ema'] = comalgo.xeam(df.adj_close)
    return df


