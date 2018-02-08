import sys
sys.path.append("..\\core")
import datehelper


import pandas as pd

from repository import stockpricerepo
from chart import stockchart

def main():
    print(datehelper.get_tbd1())

    
    df = stockpricerepo.get_stockprice('GOOG')
    stockchart.show_close_withadj(df)
    

if (__name__ == '__main__'):
    main()