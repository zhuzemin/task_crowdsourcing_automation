import os
from PyQt5.QtCore import pyqtSignal, QThread
import win32com.client

DEBUG = True


def debug(s):
    if DEBUG:
        print(s)


class FirefoxThread(QThread):
    progress_update = pyqtSignal(object)  # 信号类型 homedir = os.path.expanduser("~")
    homedir = os.path.expanduser("~")
    debug('homedir: ' + homedir)
    fxProfile_iniPath = homedir + '\\AppData\\Roaming\\Mozilla\\Firefox\\profiles.ini'
    if os.path.exists(fxProfile_iniPath):
        os.rename(fxProfile_iniPath, fxProfile_iniPath+'_bak')
    fxProfile_iniStr = '''[General]
StartWithLastProfile=1

[Profile0]
Name=iMacros
IsRelative=0
Path=''' + os.path.dirname(os.path.abspath(__file__)) + '''\\Firefox\\Profiles\\iMacros
'''
    debug('os.path.dirname(os.path.abspath(__file__)): ' + os.path.dirname(os.path.abspath(__file__)))
    fileHandle = open(fxProfile_iniPath, 'w')
    fileHandle.write(fxProfile_iniStr)
    fileHandle.close()
    debug(fxProfile_iniStr)
    iMacros = win32com.client.Dispatch("imacros")
    iMacrosScriptPath = None

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        self.DoWork()

    def DoWork(self):
        self.iMacros.iimInit('-fx -fxPath "Firefox\\firefox.exe" -fxProfile "iMacros"', True)
        if os.path.exists(self.fxProfile_iniPath+'_bak'):
            os.remove(self.fxProfile_iniPath)
            os.rename(self.fxProfile_iniPath+'_bak', self.fxProfile_iniPath)
        self.iMacros.iimPlay(self.iMacrosScriptPath + 'login.iim')
