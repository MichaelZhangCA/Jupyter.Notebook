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
        return super().__init__(**kwargs)


    @staticmethod
    def init_connection(server, db, user, pwd):
        """ have to explicit change the Class varibles, otherwise Python will automatically create new variables """
        DbConnection.servername = server
        DbConnection.database = db
        DbConnection.username = user
        DbConnection.password = pwd

    def __connectdb(self):
        print("  : log in as user " + self.username)
        cnx = mysql.connector.connect(user=self.username, password=self.password, host=self.servername, database=self.databasename)
        return cnx

    def __enter__(self):
        # make a new database connection and return
        self.cnx = self.__connectdb()
        return self.cnx

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cnx.close()