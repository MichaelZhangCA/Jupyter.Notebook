import marketindex.wikihelper as wiki
from marketindex.wikihelper import WikiPages

def load_sp500():
    page = wiki.get_wikihtml(WikiPages.url_sp500, WikiPages.file_sp500)
    data = wiki.grab_indexfromhtml(page)
    return data

def load_tsx60():
    page = wiki.get_wikihtml(WikiPages.url_tsx60, WikiPages.file_tsx60)
    data = wiki.grab_indexfromhtml(page)
    return data

