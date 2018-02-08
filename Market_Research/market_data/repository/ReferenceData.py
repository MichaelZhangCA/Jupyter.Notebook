# from repository.RepoBase import DbConnection
from repobase import DbConnection

class SymbolRepo(object):
    """
    class is child class of DbConnection, which has database connection info
    """

    def addsymbol(self, symbols):

        query = ("INSERT INTO `stock_market`.`market.symbol_list`"
                "(`symbol`, `company_name`, `exchange`, `issue_type`,`industry`, `sector`,`is_active`,`iex_id`, `source_date`)"
                "VALUES"
                "(%(symbol)s,%(name)s,'', %(type)s,'','',%(isEnabled)s,%(iexId)s, %(date)s) "
                "ON DUPLICATE KEY UPDATE "
                "`source_date` = %(date)s, `is_active` = %(isEnabled)s, `update_timestamp` = current_timestamp")

        with DbConnection() as cnx:
            cur = cnx.cursor()
            for symbol in symbols:
                cur.execute(query, symbol)
            cnx.commit()
            cur.close()
            #cnx.close()

    def get_newtickerlist(self):
        query = ("select symbol from `stock_market`.`market.symbol_list` where is_new = 1")
        with DbConnection() as cnx:
            cur = cnx.cursor()
            cur.execute(query)
            tickers = cur.fetchall()
            cur.close()

            return [tik[0] for tik in tickers]

    def update_companyinfo(self, companies):
        query = ("UPDATE `stock_market`.`market.symbol_list` set exchange=%(exchange)s, industry=%(industry)s, sector=%(sector)s, is_new=0, update_timestamp=current_timestamp WHERE symbol=%(symbol)s")
        with DbConnection() as cnx:
            cur = cnx.cursor()
            for compnay in companies:
                cur.execute(query, compnay)
            cnx.commit()
            cur.close()




