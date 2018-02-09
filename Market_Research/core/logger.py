from repobase import DbConnection

class Logger(object):

    def __init__(self, servicename, **kwargs):
        self.servicename = servicename
        return super().__init__(**kwargs)


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __get_log_sql(self, serverity, action, msg):
        query = ("INSERT INTO `stock_market`.`ops.operation_log` (`effective_date`, `service_name`, `action_name`, `serverity`, `log_message`) "
                 "VALUES  ( current_date, '{0}', '{1}', '{2}', '{3}')".format(self.servicename, action, serverity, msg.replace("'","")))
        
        return query

    def __exec_log(self, query):
        with DbConnection() as cnx:
            cur = cnx.cursor()

            # clear current record
            cur.execute(query)
            cnx.commit()
            cur.close()


    def loginfo(self,action,msg):
        query = self.__get_log_sql("I", action, msg)
        self.__exec_log(query)


    def logwarning(self,action,msg):
        query = self.__get_log_sql("W", action, msg)
        self.__exec_log(query)

    def logerror(self,action,msg):
        query = self.__get_log_sql("E", action, msg)
        self.__exec_log(query)
