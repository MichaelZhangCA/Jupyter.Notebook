from repobase import DbConnection

class Logger(object):

    def __init__(self, servicename, **kwargs):
        self.servicename = servicename
        self.query = ("INSERT INTO `stock_market`.`ops.operation_log` (`effective_date`, `service_name`, `action_name`, `serverity`, `log_message`) "
                 "VALUES  ( current_date, '{0}', %s, %s, %s)".format(self.servicename))

        return super().__init__(**kwargs)


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __get_log_sql(self):
        
        
        return query

    def __exec_log(self, serverity, action, msg):
        with DbConnection() as cnx:
            cur = cnx.cursor()

            # clear current record
            cur.execute(self.query, (action, serverity, msg))
            cnx.commit()
            cur.close()


    def loginfo(self,action,msg):
        self.__exec_log("I", action, msg)


    def logwarning(self,action,msg):
        self.__exec_log("W", action, msg)

    def logerror(self,action,msg):
        self.__exec_log("E", action, msg)
