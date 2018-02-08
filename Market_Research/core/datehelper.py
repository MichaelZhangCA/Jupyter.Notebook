import datetime
import pandas as pd
from pandas.tseries.offsets import BDay
from datetime import timedelta

def get_tbd1():
    tbd1 = pd.datetime.today() - BDay(1)
    return tbd1.to_pydatetime().date()

def get_nextday(td):
    return td + timedelta(days = 1)