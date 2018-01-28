import datetime
from repository.RepoBase import DbConnection

def __get_insert_sql(symbol):
    ins =("INSERT INTO `stock_market`.`market.stock_price` "
        "(`symbol`,`effective_date`,`open`,`high`,`low`,`close`,`volume`,`ex_dividend`,`split_ratio`,`adj_open`,`adj_high`,`adj_low`,`adj_close`,`adj_volume`) "
        "VALUES "
        "('{0}','{1}',%(Open)s,%(High)s,%(Low)s,%(Close)s,%(Volume)s,%(Ex-Dividend)s,%(Split Ratio)s,%(Adj. Open)s,%(Adj. High)s,%(Adj. Low)s,%(Adj. Close)s,%(Adj. Volume)s)"
        .format(symbol, "{}"))
    return ins

def refresh_symbolhistoric(symbol, hisdata):
    
    if (hisdata.empty):
        return

    clr = "DELETE FROM `market.stock_price` WHERE symbol = '{}'".format(symbol)

    ins = __get_insert_sql(symbol)

    with DbConnection() as cnx:
        cur = cnx.cursor()

        # clear current record
        cur.execute(clr)
        cnx.commit()

        hisdic = hisdata.to_dict(orient='index')

        # insert from the list
        for ts, row in hisdic.items():
            # put effective date to query
            query = ins.format(ts.to_pydatetime().strftime('%Y-%m-%d'))
            cur.execute(query, row)
            
        cnx.commit()
        cur.close()

def patch_symbolhistoric(symbol, hisdata):
    
    if (hisdata.empty):
        return

    # get earliest date in the patch dataset
    firstdate = hisdata.index.min()
    # print("  : will clean up data after (and equal) {0}".format(firstdate.to_pydatetime().strftime('%Y-%m-%d')))

    clr = "DELETE FROM `market.stock_price` WHERE symbol = '{0}' and effective_date >= '{1}'".format(symbol, firstdate.to_pydatetime().strftime('%Y-%m-%d'))
    # print("  : sql : {}".format(clr))

    ins = __get_insert_sql(symbol)

    with DbConnection() as cnx:
        cur = cnx.cursor()

        # clear current record
        cur.execute(clr)
        cnx.commit()

        hisdic = hisdata.to_dict(orient='index')

        # insert from the list
        for ts, row in hisdic.items():
            # put effective date to query
            query = ins.format(ts.to_pydatetime().strftime('%Y-%m-%d'))
            cur.execute(query, row)
            pass

        cnx.commit()
        cur.close()