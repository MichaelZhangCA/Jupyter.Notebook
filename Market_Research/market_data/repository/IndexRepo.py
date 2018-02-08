import datetime
#from repository.RepoBase import DbConnection
from repobase import DbConnection

def refresh_symbol(indexname, symbols):

    if (len(symbols) == 0):
        return

    cur_date = datetime.datetime.today().strftime('%Y-%m-%d')
    query = ("INSERT INTO `stock_market`.`market.index_constituent`"
            "(`index_name`, `symbol`, `start_date`, `end_date`)"
            "VALUES"
            "('{0}', %(symbol)s, '{1}', '9999-12-31') "
            "ON DUPLICATE KEY UPDATE "
            "`valid_flag`=1, `end_date`='9999-12-31', `update_timestamp`=current_timestamp").format(indexname, cur_date)

    # print (query)

    with DbConnection() as cnx:
        cur = cnx.cursor()

        # reset all valid_flag to 0
        cur.execute("UPDATE `stock_market`.`market.index_constituent` SET valid_flag=0 WHERE index_name='{0}'".format(indexname))
        cnx.commit()

        # update from the list
        # -- exists symbol will be flaged as valid = 1
        # -- new symbol will be flaged as valid = 1 with start date = today
        for symbol in symbols:
            cur.execute(query, symbol)
        cnx.commit()

        # update all invalid symbal end date as today
        cur.execute("UPDATE `stock_market`.`market.index_constituent` SET end_date = '{1}' WHERE valid_flag=0 AND index_name='{0}' AND end_date = '9999-12-31'".format(indexname, cur_date))
        cnx.commit()

        cur.close()
        #cnx.close()


def get_indexsymbollist():
    query = "SELECT symbol, max_effective_date FROM stock_market.index_symbollist"
    with DbConnection() as cnx:
        cur = cnx.cursor()

        # reset all valid_flag to 0
        cur.execute(query)
        tb = cur.fetchall()
        cur.close()

        return [(row[0], row[1]) for row in tb]
