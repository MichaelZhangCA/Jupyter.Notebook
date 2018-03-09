import mysql.connector

class DbConnection(object):
    """
    class to hold database connection information
    by default, the connection info are hard-coded
    which could be overridden by call static method "init_connection"
    """

    servername = "127.0.0.1"
    username = 'root'
    password = 'Password2017'
    databasename = 'stock_market'

    def __init__(self, **kwargs):
        # print("  : log in as user " + self.username)
        self.cnx = mysql.connector.connect(user=self.username, password=self.password, host=self.servername, database=self.databasename)
        return super().__init__(**kwargs)


    @staticmethod
    def init_connection(server, db, user, pwd):
        """ have to explicit change the Class varibles, otherwise Python will automatically create new variables """
        DbConnection.servername = server
        DbConnection.database = db
        DbConnection.username = user
        DbConnection.password = pwd

    def __connectdb(self):
        return self.cnx

    def __enter__(self):
        # make a new database connection and return
        self.cnx = self.__connectdb()
        return self.cnx

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cnx.close()



"""
    Connection class for MSSQL Server
    By default will use trust connection uner the user privilige
"""
class MssqlConnection(object):
    """
    class to hold database connection information
    by default, the connection info are hard-coded
    which could be overridden by call static method "init_connection"
    """

    servername = "PPR1EAGLESQL01.hoopp.com"
    databasename = 'PACE_HOOPP_DEV'
    #username = 'quant'
    #password = 'Password2017'

    def __init__(self, **kwargs):
        # print("  : log in as user " + self.username)
        self.cnx = pyodbc.connect("Driver={SQL Server};" + "Server=PPR1EAGLESQL01.hoopp.com;Database=PACE_HOOPP_DEV;Trusted_Connection=yes;".format(self.servername, self.databasename))
        return super().__init__(**kwargs)

    @staticmethod
    def init_connection(server, db):
        """ have to explicit change the Class varibles, otherwise Python will automatically create new variables """
        MssqlConnection.servername = server
        MssqlConnection.database = db

    def __connectdb(self):
        return self.cnx

    def __enter__(self):
        # make a new database connection and return
        self.cnx = self.__connectdb()
        return self.cnx

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cnx.close()
