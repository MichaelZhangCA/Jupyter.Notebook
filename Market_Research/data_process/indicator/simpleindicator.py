import pandas as pd
import commonalgorithm as comalgo



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
