import pandas as pd

def process_bollingerbands(dfclose):
    # get rolling 20 list
    rolling = dfclose["adj_close"].rolling(20)

    # construct return DF
    df = pd.DataFrame()
    df['adj_close'] = dfclose['adj_close']
    df['rolling'] = rolling.sum()
    df['sma20'] = rolling.mean()
    # by default, ddof is 1 which calculate sample deviation
    df['stdev'] = rolling.std(ddof=0)
    df['band_upper'] = df['sma20'] + df['stdev'] * 2
    df['band_lower'] = df['sma20'] - df['stdev'] * 2

    return df;
