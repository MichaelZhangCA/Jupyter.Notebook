# -*- coding: utf-8 -*-

import sys

# Print iterations progress
def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar

    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


class UiHelper(object):

    iteration = 0
    total = 100
    prefix = ''
    suffix = ''
    decimals = 1
    bar_length = 100

    def __init__(self, total, prefix='', suffix='', decimals=1, bar_length=100, **kwargs):
        self.iteration = 0
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.bar_length = bar_length

        return super().__init__(**kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def progress(self, iteration):

        self.iteration = iteration

        str_format = "{0:." + str(self.decimals) + "f}"
        percents = str_format.format(100 * (iteration / float(self.total)))
        filled_length = int(round(self.bar_length * iteration / float(self.total)))
        bar = '█' * filled_length + '-' * (self.bar_length - filled_length)

        sys.stdout.write('\r%s |%s| %s%s %s' % (self.prefix, bar, percents, '%', self.suffix)),

        if iteration == self.total:
            sys.stdout.write('\n')
        sys.stdout.flush()

    def progressstep(self):
        self.progress(self.iteration + 1)
