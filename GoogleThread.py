from bs4 import BeautifulSoup
import requests
from PyQt5.QtCore import pyqtSignal, QThread
from SearchResultThread import *
DEBUG = True
import time


def debug(s):
    if DEBUG:
        print(s )


class GoogleThread(QThread):
    progress_update = pyqtSignal(object)  # 信号类型
    Pause=False
    KeywordList=None
    DatabasePath=None
    ProxyEnable=False
    ProxyType=None
    Proxy=None
    Threads=[]
    ProgressBarMax=0
    ProgressBarCurrent=0
    CurrentKeywordIndex=0
    Headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        self.DoWork()

    def DoWork(self):
        s = requests.Session()
        if self.ProxyEnable:
            s.proxies = {
                'http': self.ProxyType+'://'+self.Proxy,
                'https': self.ProxyType+'://'+self.Proxy,
            }
        for keyword in self.KeywordList:
            self.ProgressBarCurrent=0
            if self.Pause:
                debug("GoogleThread Paused")
                while self.Pause: time.sleep(1)
            response=s.get('https://www.google.com/search?q='+keyword,headers=self.Headers)
            debug('response: '+response.text)
            dom=BeautifulSoup(response.text,"html.parser")
            container=dom.findAll("div", {"class": "bkWMgd"})[-1]
            searchResultList=container.findAll('div',{"class":"g"})
            self.ProgressBarMax=len(searchResultList)
            debug("self.ProgressBarMax: "+str(self.ProgressBarMax))
            for searchResult in searchResultList:
                url=searchResult.find('a')['href']
                thread=SearchResultThread(self)
                thread.progress_update.connect(self.setProgressVal)
                thread.url=url
                thread.DatabasePath=self.DatabasePath
                thread.ProxyEnable=self.ProxyEnable
                thread.ProxyType = self.ProxyType
                thread.Proxy=self.Proxy
                thread.start()
                self.Threads.append(thread)
            while self.ProgressBarCurrent<self.ProgressBarMax: time.sleep(1)
            self.CurrentKeywordIndex=self.CurrentKeywordIndex+1
            debug("self.ProgressBarMax: "+str(self.ProgressBarMax))
            #time.sleep(3)

    def PauseSubThread(self):
        for thread in self.Threads:
            thread.Pause=self.Pause


    def setProgressVal(self,val):
        debug("self.ProgressBarCurrent: "+str(self.ProgressBarCurrent))

        val['CurrentKeywordIndex']=self.CurrentKeywordIndex
        val['ProgressBarMax']=self.ProgressBarMax
        self.ProgressBarCurrent=self.ProgressBarCurrent+1
        val['ProgressBarCurrent']=self.ProgressBarCurrent
        self.progress_update.emit(val)


    def TerminateSubThread(self):
        for thread in self.Threads:
            thread.terminate()
