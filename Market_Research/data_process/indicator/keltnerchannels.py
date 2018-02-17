import pandas as pd

def process_keltnerchannels(df):
    
    # ==> 20 days EWMA
    ema_period = 20
    ema_rolling = df[:ema_period]["adj_close"].rolling(ema_period)

    # combine the first SMA with the rest close adj price
    ema_con = pd.concat([ema_rolling.mean(), df[ema_period:]['adj_close']])
    #con.head(30)

    df['ema_con'] = ema_con
    df['ema20'] = ema_con.ewm(span=ema_period, adjust=False).mean()
    
    # ==> 10 days ATR
    atr_period = 10

    # prepare TR for each day
    df['h_l'] = df['adj_high'] - df ['adj_low']
    df['h_pc'] = abs(df['adj_high'] - df ['adj_close'].shift(1))
    df['l_pc'] = abs(df['adj_low'] - df ['adj_close'].shift(1))
    df['TR'] = df[['h_l','h_pc','l_pc']].max(axis=1)

    # get the first SMA for the rolling windows
    atr_rolling = df[:atr_period]["TR"].rolling(atr_period)

    # combine the first SMA with the rest close adj price
    tr_con = pd.concat([atr_rolling.mean(), df[atr_period:]['TR']])
    df['tr_con'] = tr_con
    atr_cal = (df['tr_con'].shift(1) * (atr_period-1) + df['tr_con']) / atr_period
    df['atr_cal'] = atr_cal
    # merge the first SMA with the rest ATR
    df['atr10'] = pd.concat([tr_con[:atr_period], atr_cal[atr_period:]])


    # ==> assign upper/lower band
    df['atr1_upper'] = df['ema20'] + df['atr10'] 
    df['atr1_lower'] = df['ema20'] - df['atr10']
    df['atr2_upper'] = df['ema20'] + df['atr10'] * 2
    df['atr2_lower'] = df['ema20'] - df['atr10'] * 2
    df['atr3_upper'] = df['ema20'] + df['atr10'] * 3
    df['atr3_lower'] = df['ema20'] - df['atr10'] * 3

    return df;

