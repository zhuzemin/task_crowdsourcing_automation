import time


class iMacrosLibrary():
    Pause=False
    DEBUG = False
    stepInterval = 0
    iMacros=None

    def __init__(self,DEBUG,stepInterval,iMacros):
        self.DEBUG=DEBUG
        self.stepInterval=stepInterval
        self.iMacros=iMacros

    def debug(self,s):
        if self.DEBUG:
            print(s)

    def iimAddWait(self,iimPath):
        with open(iimPath, 'r') as f:
            iimStr = f.read()
        if iimPath.endswith('.iim') and self.DEBUG:
            iimStr = iimStr.replace('\n','\nWAIT SECONDS='+self.stepInterval+'\n')
            self.debug('iimStr: '+iimStr)
        return iimStr

    def iimPlay(self,iimPath):
        with open(iimPath, 'r') as f:
            iimList = f.readlines()
        for line in iimList:
            if self.Pause:
                while self.Pause: time.sleep(1)
            self.iMacros.iimPlayCode(line)
            if self.DEBUG:
                time.sleep(self.stepInterval)
