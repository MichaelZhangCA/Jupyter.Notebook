import pandas as pd

# cross reference
from datarepository import stockpricerepo
import uihelper

from indicator import trend_indicator as trendidc, volatility_indicator as volidc


# default JC parameters
DEFAULT_JC_PRAM = {
    'sma_period':20,
    'dev_mode':'std',
    'ema_period':20,
    'atr_mode':'atr',
    'atr_period':14,
    'macd':'12/26/9',
    'wavebase':8,
    'wavea':34,
    'waveb':89,
    'wavec':233
    }

""" Live calcualte John Carter TTM Squeeze indicator based on full history adjusted price
"""
def process_jcsqueeze(symbol, jcpara=DEFAULT_JC_PRAM):

    # load stock price
    df = stockpricerepo.get_stock_adjprice(symbol)
    
    # live calculate Bollings Band
    sma, stdev, smpldev = trendidc.process_sma(df.adj_close, jcpara['sma_period'])
    df['bb_middle'] = sma
    if (jcpara['dev_mode'] == 'std'):
        df['bb_upper'] = sma + stdev * 2
        df['bb_lower'] = sma - stdev * 2
    else:
        df['bb_upper'] = sma + smpldev * 2
        df['bb_lower'] = sma - smpldev * 2
    
    # Keltner Channel
    ema = trendidc.process_ema(df.adj_close, jcpara['ema_period'])
    df['kc_middle'] = ema
    if (jcpara['atr_mode']=='atr'):
        atr = volidc.process_atr(df, jcpara['atr_period'])
        df['kc_upper'] = ema + atr * 2
        df['kc_lower'] = ema - atr * 2
    else:
        ematr = volidc.process_ematr(df, jcpara['atr_period'])
        df['kc_upper'] = ema + ematr * 2
        df['kc_lower'] = ema - ematr * 2

    # MACD
    macd_periods = jcpara['macd'].split('/')
    emashort = trendidc.process_ema(df.adj_close, int(macd_periods[0]))
    emalong = trendidc.process_ema(df.adj_close, int(macd_periods[1]))
    macd = trendidc.process_macd(emashort, emalong, int(macd_periods[2]))
    df['macd'] = macd

    # WAVE A/B/C
    emabase = trendidc.process_ema(df.adj_close, jcpara['wavebase'])
    emawavea = trendidc.process_ema(df.adj_close, jcpara['wavea'])
    emawaveb = trendidc.process_ema(df.adj_close, jcpara['waveb'])
    emawavec = trendidc.process_ema(df.adj_close, jcpara['wavec'])

    df['wavea'] = trendidc.process_macd(emabase, emawavea, jcpara['wavea'])
    df['waveb'] = trendidc.process_macd(emabase, emawavea, jcpara['waveb'])
    df['wavec'] = trendidc.process_macd(emabase, emawavea, jcpara['wavec'])

    return df
    pass

