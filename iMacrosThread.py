import sqlite3
import requests
import time
from bs4 import BeautifulSoup
from PyQt5.QtCore import pyqtSignal, QThread


class iMacrosThread(QThread):
    progress_update = pyqtSignal(object)  # 信号类型
    Pause = False
    MatchingRuleObjectList = []
    DatabasePath = None
    ProxyEnable = False
    ProxyType = None
    Proxy = None
    Headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}
    iMacros = None
    iMacrosScriptPath = None
    Threads = []
    queueRulePath = None
    queueName = None
    stepInterval = 0
    DEBUG = False
    extractList = []

    def debug(self, s):
        if self.DEBUG:
            print(s)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        self.DoWork()

    def DoWork(self):
        submitCount=0
        while self.Pause is not True:
            self.iimToListPlay(self.iMacrosScriptPath + "getKeyword.iim")
            title=self.extractList[0]
            description=self.extractList[1]
            self.debug('title: ' + title)
            self.debug("description: " + description)
            if title != 'NODATA' and description != "NODATA":
                SearchKeywordList = [title, description, title + ' ' + description]
                if self.DEBUG is not True:
                    s = requests.Session()
                    if self.ProxyEnable:
                        s.proxies = {
                            'http': self.ProxyType + '://' + self.Proxy,
                            'https': self.ProxyType + '://' + self.Proxy,
                        }
                for SearchKeyword in SearchKeywordList:
                    if self.Pause:
                        while self.Pause: time.sleep(1)
                    if self.DEBUG:
                        self.iimToListPlay(self.iMacrosScriptPath + "google.iim",[{"keyword":SearchKeyword}])
                        if len(self.extractList) > 0:
                            rhs=self.extractList[0]

                    else:
                        response = s.get('https://www.google.com/search?q=' + SearchKeyword, headers=self.Headers)
                        self.debug('response: ' + response.text)
                        dom = BeautifulSoup(response.text, "html.parser")
                        rhs = dom.find(id='rhs').string
                    self.debug('rhs: '+rhs)
                    if rhs is None:
                        continue
                    elif SearchKeyword == SearchKeywordList[-1] and rhs is None:  # manual
                        self.debug(str(self.MatchingRuleObjectList))
                        break
                    else:
                        currentMatchingRuleObjectIndex=0
                        for MatchingRuleObject in self.MatchingRuleObjectList:
                            if self.Pause:
                                while self.Pause: time.sleep(1)
                            self.debug("MatchingRuleObject['filename']: " + MatchingRuleObject['filename'])
                            if MatchingRuleObject['avairable'] == True:
                                matchKeywordCount = 0
                                for keyword in MatchingRuleObject['matchingKeywordList']:
                                    if keyword in rhs:
                                        matchKeywordCount = matchKeywordCount + 1
                                        if matchKeywordCount == MatchingRuleObject['matchKeywordNum']:
                                            self.debug("MatchingRuleObject['specialCondition']: "+MatchingRuleObject['specialCondition'])
                                            if MatchingRuleObject['specialCondition'] != "":
                                                self.debug('specialCondition')
                                                self.iMacros.iimPlayCode(MatchingRuleObject['specialCondition'])
                                                correctCategoryStr = self.iMacros.iimGetExtract(1)
                                                self.debug('correctCategoryStr: '+correctCategoryStr)
                                                #correctCategoryStr=eval(MatchingRuleObject['specialCondition'])# execute specialCondition
                                                for categoryStr in MatchingRuleObject['categoryStrList']:
                                                    if categoryStr != correctCategoryStr:
                                                        MatchingRuleObject['categoryStrList'].remove(categoryStr)
                                            self.iMacros.iimPlayCode('TAB CLOSE')
                                            self.debug("MatchingRuleObject['categoryStrList']: "+str(MatchingRuleObject['categoryStrList']))
                                            if self.DEBUG:
                                                self.Pause = True
                                                progressObject = {
                                                    'threadStatus': 'pause'
                                                }
                                                self.progress_update.emit(progressObject)
                                                if self.Pause:
                                                    while self.Pause: time.sleep(1)
                                            # self.iMacros.iimPlayCode()  # submit
                                            for categoryStr in MatchingRuleObject['categoryStrList']:
                                                self.iimToListPlay(self.iMacrosScriptPath + "answering.iim",
                                                       [{"categoryStr": categoryStr.replace(' ', '<SP>')}])
                                break
                            currentMatchingRuleObjectIndex = currentMatchingRuleObjectIndex+1
                        conn = sqlite3.connect(self.DatabasePath)  # 建立数据库连接
                        cu = conn.cursor()
                        cu.execute('INSERT OR IGNORE INTO '+self.queueName+' (title,description,searchResult) VALUES (?,?,?)',
                        (title, description,rhs))
                        conn.commit()  # 提交更改
                        conn.close()  # 关闭数据库连接
                        submitCount = submitCount + 1
                        progressObject['threadStatus']='done'
                        progressObject['searchResult']={
                                'title': title,
                                'description': description,
                                'googleResult': rhs,
                                'currentMatchingRuleObjectIndex': currentMatchingRuleObjectIndex
                            }
                        progressObject['submitCount']=submitCount
                        self.progress_update.emit(progressObject)
                        break
            else:
                self.debug('[Error]title or description extract failed')

    def PauseSubThread(self):
        for thread in self.Threads:
            thread.Pause = self.Pause

    '''def setProgressVal(self, val):
        debug("self.ProgressBarCurrent: " + str(self.ProgressBarCurrent))

        val['CurrentKeywordIndex'] = self.CurrentKeywordIndex
        val['ProgressBarMax'] = self.ProgressBarMax
        self.ProgressBarCurrent = self.ProgressBarCurrent + 1
        val['ProgressBarCurrent'] = self.ProgressBarCurrent
        self.progress_update.emit(val)'''

    def TerminateSubThread(self):
        for thread in self.Threads:
            thread.terminate()

    def iimToListPlay(self,iimPath,iimValueObjectList=None):
        with open(iimPath, 'r') as f:
            iimList = f.readlines()
        self.extractList.clear()
        for line in iimList:
            if self.Pause:
                while self.Pause: time.sleep(1)
            if(iimValueObjectList is not None):
                for iimValueObject in iimValueObjectList:
                    for key, value in iimValueObject.items():
                        self.iMacros.iimSet(key,value)
            self.iMacros.iimPlayCode(line)
            if self.iMacros.iimGetExtract(1) != 'NODATA':
                self.debug('self.iMacros.iimGetExtract(1): '+self.iMacros.iimGetExtract(1))
                self.extractList.append(self.iMacros.iimGetExtract(1))
            if self.DEBUG:
                time.sleep(int(self.stepInterval))
