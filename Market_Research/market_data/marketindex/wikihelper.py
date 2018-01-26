import marketindex
import requests
import os
import datetime
import sys
import pprint
import csv
import re
from bs4 import BeautifulSoup
import pandas as pd

class WikiPages(object):

    url_sp500 = "List_of_S%26P_500_companies"
    url_tsx60 = "S%26P/TSX_60"

    file_sp500 = "sp500"
    file_tsx60 = "tsx60"


def save_csv(filename, datalist):
    filepath = os.path.dirname(marketindex.__file__) + "\\cached\\" + filename + "." + datetime.datetime.today().strftime('%Y%m%d') + ".csv"

    df = pd.DataFrame(datalist)
    df.to_csv(filepath, sep=',', encoding='utf-8', index=False)

    """
    with open(filename, "w") as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL, lineterminator='\n', delimiter=',')
        wr.writerows(datalist)
        #for row in datalist:
        #    wr.writerow(row.symbol, row.company)
    """

def save_html(filename, filedata):
    filepath = os.path.dirname(marketindex.__file__) + "\\cached\\" + filename + "." + datetime.datetime.today().strftime('%Y%m%d') + ".html"

    with open(filepath, "wb") as savedfile:
        savedfile.write(filedata)

def get_wikihtml(wikipage, filename):
    '''
    Obtains html from Wikipedia
    Note: API exist but for my use case. Data returned was not parsable. Preferred to use html
    python-wikitools - http://code.google.com/p/python-wikitools/
    Ex. http://en.wikipedia.org/w/api.php?format=xml&action=query&titles=List_of_S%26P_500_companies&prop=revisions&rvprop=content
    '''

    wiki_html = requests.get('http://en.wikipedia.org/wiki/{}'.format(wikipage))

    if (filename != ""):
        # Save file to be used by cache
        save_html(filename, wiki_html.content)
    return wiki_html.content

def grab_indexfromhtml(page_html, filename):
    wiki_soup = BeautifulSoup(page_html, "html.parser")
    symbol_table = wiki_soup.find(attrs={'class': 'wikitable sortable'})

    symbol_data_list = list()

    for symbol in symbol_table.find_all("tr"):
        symbol_data_content = dict()
        symbol_raw_data = symbol.find_all("td")
        td_count = 0
        for symbol_data in symbol_raw_data:
            if(td_count == 0):
                symbol_data_content['symbol'] = symbol_data.text
            elif(td_count == 1):
                symbol_data_content['company'] = symbol_data.text

            td_count += 1

        if (bool(symbol_data_content)):
            symbol_data_list.append(symbol_data_content)

    if (filename != ""):
        #write csv file
        save_csv(filename, symbol_data_list)

    # skip table header
    return symbol_data_list

