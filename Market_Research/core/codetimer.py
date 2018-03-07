from time import time, strftime, localtime
from datetime import timedelta

class CodeTimer(object):

    recentlog = ""

    def __init__(self, codesnip='== default wrap codes ==', **kwargs):
        self.codesnip = codesnip
        return super().__init__(**kwargs)

    def __enter__(self):
        self.start = time()
        #atexit.register(self.__endlog)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__endlog()


    def __endlog(self):
        self.end = time()
        self.elapsed = self.end - self.start

        CodeTimer.recentlog = "[ {} ] executed in {}".format(self.codesnip, self.__secondsToStr(self.elapsed))
        print(CodeTimer.recentlog)

    def __secondsToStr(self, elapsed):
        return str(timedelta(seconds=elapsed))
