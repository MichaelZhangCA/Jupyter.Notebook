import pandas as pd

def process_macd(shortema, longema, signalperiod):

    # alwasy duplicate index from the short ema, it will make sure date coverage
    df = pd.DataFrame(index=shortema.index)
    df['short_ema'] = shortema.ema
    df['long_ema'] = longema.ema
    df['macd'] = shortema - longema
    df['macd_ema'] = df.macd.ewm(span=signalperiod, adjust=False).mean()
    df['macd_histogram'] = df.macd - df.macd_ema

    return df

