import pandas as pd

# process EMA for x days
def process_ema(df, period):
    
    # roll the first x days for fist SMA start point
    ema_rolling = df[:period]["adj_close"].rolling(period)

    # combine the first SMA with the rest close adj price
    ema_con = pd.concat([ema_rolling.mean(), df[period:]['adj_close']])
    #con.head(30)
    #df['ema_con'] = ema_con
    df['ema'] = ema_con.ewm(span=period, adjust=False).mean()
    return df
