import pandas as pd
from repository import stockpricerepo
from chart import stockchart
import datehelper

def show_stockchart():
   
    df = stockpricerepo.get_stockprice('GOOG')
    stockchart.show_close_withadj(df)
    

if (__name__ == '__main__'):
    show_stockchart()