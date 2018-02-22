import adhoc_process as adhoc

def process_keltnerchannels(symbol, ema_period, atr_period):
    # patch all base indicator
    adhoc.patch_symbol_ema(symbol, ema_period)
    adhoc.patch_symbol_atr(symbol, atr_period)

    # once patching process is done, the KC could be retrieved from view directly


def process_bollingerbands(symbol, period):
    # patch base indicator, stdev is included in sma patching
    adhoc.patch_symbol_sma(symbol, period)

    # once patching process is done, the KC could be retrieved from view directly
