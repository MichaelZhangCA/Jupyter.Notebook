"""
Trend indicators measure the direction and strength of a trend
using some form of price averageing to establish a baseline

Typical treand indicator includes:
  - SMA / EMA
  - MACD / PPO (Percentage Price Oscillator): PPO is percentage of MACD, which makes it's possible for comparision between stocks
  - Parabolic SAR - this is a LEADING indicator
"""
import pandas as pd
from . import common_algorithm as comalgo

# process SMA / Deviation for x days
def process_sma(x, period):
    
    # get rolling list
    rolling = x.rolling(period)

    # construct return DF
    sma = rolling.mean()
    # by default, ddof is 1 which calculate sample deviation
    stdev = rolling.std(ddof=0)
    smpldev = rolling.std(ddof=1)

    return sma, stdev, smpldev


""" Process EMA for given period
    Passed in series is adjusted clse price
"""
def process_ema(x, period, ema=None ):
    
    """
    Assumption of the imput DataFrame will have adj_close as the source
    it migh have ema column, or not.
    - if there is no ema column, it will be a full steps calculation start from rolling the first SMA as the biginning
    - if there is an ema column, then check if there is value in it
      - idealy there will be only one ema value at the very first position (row 0), then merge this ema value with the rest of price volumn as source for calculation
      - if there is no vlaue in ema column, then will go for full steps calculation again
      - if there are more than 1 value in ema column, the last ema value will be pull out and merge with rest price as the source column, 
        when getting ema calucation result back, merge with the previous ema rows
    """

    if (ema is not None):
        # if there is value then it will start be NOT a full run
        if not (ema.isnull().all()):
            # call the quick calculation from given ema value
            return comalgo.cema(x, ema, period)

    # it's not decent structure but easier to handle the variables
    # no ema and will conduct a full calculation
    return comalgo.xema(x, period)


""" Process MACD by given short EMA, long EMA and signal period
    - if no macd_eam passed in, will process full calculation, which means will be NO macd value for the first {period} rows
    - if macd_eam passed in, will base pass {macd} and {macd_ema} to process a patching process
def process_macd(shortema, longema, signalperiod, macd_ema = None):

    # alwasy duplicate index from the short ema, it will make sure date coverage
    df = pd.DataFrame(index=shortema.index)
    df['short_ema'] = shortema.ema
    df['long_ema'] = longema.ema
    df['macd'] = shortema - longema
    # df['macd_ema'] = df.macd.ewm(span=signalperiod, adjust=False).mean()
    if (macd_ema is None):
        df['macd_ema'] = comalgo.xeam(df.macd, signalperiod)
    else:
        df['macd_ema'] = comalgo.ceam(df.macd, macd_ema, signalperiod)
    df['macd_histogram'] = df.macd - df.macd_ema

    return df
"""

""" Calculate MACD by given short EMA, long EMA and signal period
    - the calculation is live and typically take less than 0.2 second
    - only return MACD histogram series for better flexibility
"""
def process_macd(shortema, longema, signalperiod):

    # alwasy duplicate index from the short ema, it will make sure date coverage
    #df = pd.DataFrame(index=shortema.index)
    #df['short_ema'] = shortema
    #df['long_ema'] = longema
    macd = shortema - longema
    # df['macd_ema'] = df.macd.ewm(span=signalperiod, adjust=False).mean()
    macd_ema = comalgo.xema(macd, signalperiod)
    return macd - macd_ema


""" Calculate PPO by given short EMA, long EMA and signal period
    - the calculation is live and typically take less than 0.2 second
    - only return PPO histogram series for better flexibility
"""
def process_ppo(shortema, longema, signalperiod):

    # alwasy duplicate index from the short ema, it will make sure date coverage
    ppo = (shortema - longema) / longema
    # df['macd_ema'] = df.macd.ewm(span=signalperiod, adjust=False).mean()
    ppo_ema = comalgo.xema(ppo, signalperiod)
    return ppo - ppo_ema


""" TBD - Parabolic Stop And Reverse (SAR)
"""