from bs4 import BeautifulSoup
import requests
from PyQt5.QtCore import pyqtSignal, QThread
import sqlite3
import time

DEBUG = True


def debug(s):
    if DEBUG:
        print(s )


class SearchResultThread(QThread):
    progress_update = pyqtSignal(object)  # 信号类型
    Pause=False
    DatabasePath=None
    ProxyEnable=False
    ProxyType=None
    Proxy=None
    url=None
    Headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        self.DoWork()

    def DoWork(self):
        if self.Pause:
            debug("SearchResultThread Paused")
            while self.Pause: time.sleep(1)
        s = requests.Session()
        if self.ProxyEnable:
            s.proxies = {
                'http': self.ProxyType+'://'+self.Proxy,
                'https': self.ProxyType+'://'+self.Proxy,
            }
        try:
            response=s.get(self.url,headers=self.Headers,timeout=10)
            #debug('response: '+response.text)
            dom=BeautifulSoup(response.text,"html.parser")
            conn = sqlite3.connect(self.DatabasePath)  # 建立数据库连接
            cu = conn.cursor()
            cu.execute("""INSERT OR IGNORE INTO SearchResult (name,rank,address,phone,web) VALUES (?,?,?,?,?)""",
            (dom.find('title').string, 0,None,0,self.url))
            conn.commit()  # 提交更改
            conn.close()  # 关闭数据库连接
            self.progress_update.emit({
                'searchResult':{
                    'name':dom.find('title').string,
                    'web':self.url
                }
            })
        except requests.exceptions.RequestException:
            self.progress_update.emit({
                'searchResult':{
                    'name':'Faile',
                    'web':self.url
                }
            })
