"""
Volatility indicators measure the rate of price movement, regardless of direction.

Typical momentum indicator includes the followings and they are all LAGGING indecator
  - Bollinger Bands (will move to combination indicators)
  - Average True Range (ATR): it's not a indicator for price trend, it's the degree of price volativity.
  - Standard Deviation (population deviation and sample deviation are calculated with SMA)
"""
import pandas as pd
from . import common_algorithm as comalgo


""" Process ATR for given period
    Assume passed in DataFrame will have "adj_open","adj_high","adj_low" and "adj_close"
    Optional could have "atr" column if already exists
    - with exists "atr" column and at least one value, will NOT do rolling for the first SMA
"""
def process_atr(dfprice, period, atr=None):

    dft = pd.DataFrame(index = dfprice.index)
    # prepare TR for each day
    dft['h_l'] = dfprice['adj_high'] - dfprice ['adj_low']
    dft['h_pc'] = abs(dfprice['adj_high'] - dfprice ['adj_close'].shift(1))
    dft['l_pc'] = abs(dfprice['adj_low'] - dfprice ['adj_close'].shift(1))
    tr = dft[['h_l','h_pc','l_pc']].max(axis=1)

    fullcalculation = True
    if (atr is not None):
        # if there is value then it will start be NOT a full run
        if not (atr.isnull().all()):
            fullcalculation = False

    if (fullcalculation):
        # get the first SMA for the rolling windows (only roll niminal rows so make sure only one SMA is calculated
        atr_rolling = tr[:period].rolling(period)

        # combine the first SMA with the rest TR
        TR_con = pd.concat([atr_rolling.mean(), tr[period:]])
    
        for i in range(1, len(TR_con)):
            if (not pd.isnull(TR_con[i-1])):
                TR_con[i] = ( TR_con[i-1] * (period-1) + TR_con[i] ) / period

        return TR_con.rename('atr')

    else:
        # locate the last atr postion
        last_pos = dfprice.index.get_loc(atr.last_valid_index())
        # cur off the previous ema valus as reserv part
        exist_atr = atr[:last_pos]   # right side is not included
        
        # merge the last atr with the rest of TR
        merge_TR = pd.concat([atr[last_pos:last_pos+1], tr[last_pos+1:]])
        
        # calculate TR from the 2nd row
        for i in range(1, len(merge_TR)):
            merge_TR[i] = ( merge_TR[i-1] * (period-1) + merge_TR[i] ) / period
    
        # merge the reserved atr values with calculated values
        return pd.concat([exist_atr, merge_TR]).rename('atr')

  


""" Process EMA-TR for given period
    - formula of ATR will simply use EMA calculation on TR column
    Assume passed in DataFrame will have "adj_open","adj_high","adj_low" and "adj_close"
    Optional could have "ematr" column if already exists
    - with exists "atr" column and at least one value, will NOT do rolling for the first SMA
"""
def process_ematr(df, period):

    dft = pd.DataFrame(index = df.index)
    # prepare TR for each day
    dft['h_l'] = df['adj_high'] - df ['adj_low']
    dft['h_pc'] = abs(df['adj_high'] - df ['adj_close'].shift(1))
    dft['l_pc'] = abs(df['adj_low'] - df ['adj_close'].shift(1))
    dft['TR'] = dft[['h_l','h_pc','l_pc']].max(axis=1)

    fullcalculation = True
    if ('atr' in df.columns):
        # if there is value then it will start be NOT a full run
        if not (df.atr.isnull().all()):
            fullcalculation = False

    ematr = None
    if (fullcalculation):
        ematr = comalgo.xema(dft.TR, period)
    else:
        ematr = comalgo.cema(dft.TR, df.ematr, period)

    return ematr.rename('ematr')
