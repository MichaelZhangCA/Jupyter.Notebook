import pandas as pd

# process SMA / STDEV for x days
def process_sma(df, period):
    
    # get rolling list
    rolling = df["adj_close"].rolling(period)

    # construct return DF
    df['sma'] = rolling.mean()
    # by default, ddof is 1 which calculate sample deviation
    df['stdev'] = rolling.std(ddof=0)

    return df


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


# process ATR for x days
def process_atr(df, period):

    # prepare TR for each day
    df['h_l'] = df['adj_high'] - df ['adj_low']
    df['h_pc'] = abs(df['adj_high'] - df ['adj_close'].shift(1))
    df['l_pc'] = abs(df['adj_low'] - df ['adj_close'].shift(1))
    df['TR'] = df[['h_l','h_pc','l_pc']].max(axis=1)

    # get the first SMA for the rolling windows
    atr_rolling = df[:period]["TR"].rolling(period)

    # combine the first SMA with the rest close adj price
    tr_con = pd.concat([atr_rolling.mean(), df[period:]['TR']])
    df['tr_con'] = tr_con
    
    for i in range(1, len(tr_con)):
        if (not pd.isnull(tr_con[i-1])):
            tr_con[i] = ( tr_con[i-1] * (period-1) + tr_con[i] ) / period

    # tr_con has been trasformed to ATR
    df['atr'] = tr_con
    
    return df
