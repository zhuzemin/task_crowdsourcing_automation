import glob
import sys

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QFileDialog, QLineEdit, QGroupBox, QAction
from PyQt5 import QtWidgets
from MainWindow import Ui_MainWindow
# from SeleniumWorker import *
# from GoogleThread import *
from iMacrosThread import *
from loadMatchingRule import *
from FirefoxThread import *
from tkinter import Tk
from tkinter.filedialog import askdirectory

class Main(QtWidgets.QMainWindow):
    ConfigPath = 'config.ini'
    DatabasePath = 'log.db'
    thread = None
    MatchingRuleObjectList = []
    listView_ResultModel = QStandardItemModel()
    queueRulePath = None
    queueName = None
    iMacrosScriptPath = os.path.dirname(os.path.abspath(__file__)) + '\\iMacrosScript\\'
    Firefox = None

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_queueRuleBrowser.clicked.connect(lambda: self.selectFolderDialog("queueRulePath"))
        self.ui.pushButton_Start.clicked.connect(lambda: self.ThreadControl("Start"))
        self.ui.pushButton_Pause.clicked.connect(self.thread_pause_resume)
        self.ui.pushButton_Cancel.clicked.connect(lambda: self.ThreadControl("Terminate"))
        self.ui.pushButton_SaveToDB.setVisible(False)
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setVisible(False)
        # self.ui.checkBox_ProxyEnable.stateChanged.connect(self.checkBox_isChecked)
        # self.thread = SeleniumWorker(self) # 创建一个线程
        self.listView_ResultModel.insertRow(0, QStandardItem('[title] ---- [description] ---- [googleResult]'))
        self.ui.listView_Result.setModel(self.listView_ResultModel)
        self.ui.lineEdit_queueRulePath.textChanged.connect(lambda: self.handle_listView(self.ui.lineEdit_queueRulePath.text()))
        # LatestProfile=self.FindLastModifiedFile(os.path.dirname(os.path.abspath(__file__)),"\*.json")
        # if LatestProfile!=None:
        #    self.loadConfig(LatestProfile)
        # self.ui.actionLoad_Profile.triggered.connect(self.MakeopenFileNameDialog("ProfileLoad"))
        # self.ui.actionSave_Profile.triggered.connect(lambda:self.saveFileDialog("ProfileSave"))
        if len(sys.argv) > 1:
            if sys.argv[1] == '-c' and os.path.exists(sys.argv[2]):
                self.ConfigPath = sys.argv[2]
        if os.path.exists(self.ConfigPath):
            self.loadConfig(self.ConfigPath)
        QAction("Quit", self).triggered.connect(self.closeEvent)
        self.queueName = self.ui.lineEdit_queueRulePath.text().split('/')[-1]
        debug('queueName: ' + self.queueName)
        self.createDB(self.DatabasePath,self.queueName)
        self.Firefox = FirefoxThread(self)  # 创建一个线程
        self.Firefox.iMacrosScriptPath = self.iMacrosScriptPath
        self.Firefox.start()

    def handle_listView(self,folderPath):
        if os.path.exists(folderPath):
            self.MatchingRuleObjectList = loadMatchingRule(folderPath).MatchingRuleObjectList
            self.MatchingRuleObjectList.sort(key=lambda x: x['priority'], reverse=False)
            mode = QStandardItemModel()
            mode.insertRow(0, QStandardItem('[categoryStrlist] ---- filename'))
            self.ui.listView_matchingRule.setModel(mode)
            for MatchingRuleObject in self.MatchingRuleObjectList:
                Line = QStandardItem(str(MatchingRuleObject['categoryStrList']) + ' ---- ' + MatchingRuleObject['filename'])
                mode.appendRow(Line)
        else:
            debug('folderPath not exist: '+folderPath)

    def createDB(self, DatabasePath,tableName):
        conn = sqlite3.connect(DatabasePath)  # 建立数据库连接
        cu = conn.cursor()
        cu.execute("""
        CREATE TABLE IF NOT EXISTS """+tableName+""" (
        logtime TIMESTAMP default (datetime('now', 'localtime')), 
        title string, 
        description string, 
        searchResult string               
        );
        """)
        conn.commit()  # 提交更改
        conn.close()  # 关闭数据库连接

    def closeEvent(self, event):
        self.Firefox.iMacros.iimClose()
        self.saveConfig(self.ConfigPath)
        self.Firefox.terminate()
        self.setWindowTitle(self.windowTitle()+' ---- Closing...')
        time.sleep(3)

    def saveFileDialog(self, flag):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "Support Files (*.txt);;All Files (*)", options=options)
        # if fileName:
        #    if flag=="ProfileSave":
        #        self.saveConfig(fileName)

    def saveConfig(self, filePath):
        debug("saveConfig")
        config = {}
        config["Proxy"] = self.ui.lineEdit_Proxy.text()
        config["queueRulePath"] = self.ui.lineEdit_queueRulePath.text()
        config["ProxyEnable"] = self.ui.checkBox_ProxyEnable.isChecked()
        if self.ui.radioButton_ProxyTypeHttp.isChecked():
            config["ProxyType"] = "http"
        elif self.ui.radioButton_ProxyTypeSocks5.isChecked():
            config["ProxyType"] = "socks5"
        else:
            config["ProxyType"] = None
        config["DatabasePath"] = self.DatabasePath
        config['debugEnable'] = self.ui.checkBox_debugEnable.isChecked()
        config['stepInterval'] = self.ui.lineEdit_stepInterval.text()
        with open(filePath, 'w') as outfile:
            json.dump(config, outfile)

    def loadConfig(self, filePath):
        with open(filePath, 'r') as f:
            config = json.loads(f.read())
        self.ui.lineEdit_queueRulePath.setText('')
        self.ui.lineEdit_queueRulePath.setText(config["queueRulePath"])
        self.ui.lineEdit_Proxy.setText(config["Proxy"])
        self.ui.checkBox_ProxyEnable.setChecked(config["ProxyEnable"])
        if config["ProxyType"].lower() == "http":
            self.ui.radioButton_ProxyTypeHttp.setChecked(True)
        elif config["ProxyType"].lower() == "socks5":
            self.ui.radioButton_ProxyTypeSocks5.setChecked(True)
        self.DatabasePath = config["DatabasePath"]
        self.ui.checkBox_debugEnable.setChecked(config['debugEnable'])
        self.ui.lineEdit_stepInterval.setText(config['stepInterval'])

    def FindLastModifiedFile(self, Directory, FileType):
        list_of_files = glob.glob(Directory + FileType)  # * means all if need specific format then *.csv
        try:
            latest_file = max(list_of_files, key=os.path.getctime)
        except:
            return None
        return latest_file

    # def radioButton_clicked(self,flag):
    #    self.thread.ProxyType=flag

    # def checkBox_isChecked(self):
    #    if self.ui.checkBox_UseProxie.isChecked():
    #        self.ui.groupBox_Proxies.setEnabled(True)
    #    else:
    #        self.ui.groupBox_Proxies.setEnabled(False)

    def thread_pause_resume(self):
        if self.ui.pushButton_Pause.text() == "Pause":
            self.thread.Pause = True
            self.thread.PauseSubThread()
            self.ui.pushButton_Pause.setText("Resume")
        else:
            self.thread.Pause = False
            self.thread.PauseSubThread()
            self.ui.pushButton_Pause.setText("Pause")

    def ThreadControl(self, Trriger):
        if Trriger == "Start":
            # self.thread = GoogleThread(self)  # 创建一个线程
            self.thread = iMacrosThread(self)  # 创建一个线程
            self.thread.DEBUG=self.ui.checkBox_debugEnable.isChecked()
            self.thread.stepInterval=self.ui.lineEdit_stepInterval.text()
            self.thread.iMacros = self.Firefox.iMacros
            self.thread.iMacrosScriptPath = self.iMacrosScriptPath
            self.thread.queueRulePath=self.queueRulePath
            self.thread.queueName=self.queueName
            self.thread.progress_update.connect(self.setProgressVal)
            self.thread.MatchingRuleObjectList = self.MatchingRuleObjectList
            self.thread.DatabasePath = self.DatabasePath
            self.thread.ProxyEnable = self.ui.checkBox_ProxyEnable.isChecked()
            if self.ui.radioButton_ProxyTypeHttp.isChecked():
                self.thread.ProxyType = "http"
            elif self.ui.radioButton_ProxyTypeSocks5.isChecked():
                self.thread.ProxyType = "socks5"
            self.thread.Proxy = self.ui.lineEdit_Proxy.text()
            self.thread.start()
            self.ui.pushButton_Start.setEnabled(False)
        elif Trriger == "Terminate":
            self.thread.TerminateSubThread()# terminate SearchResultThread
            self.thread.terminate()# terminate GoogleThread
            self.ui.progressBar.setValue(0)
            self.ui.pushButton_Start.setEnabled(True)

    def setProgressVal(self, val):
        if val['threadStatus'] == 'pause':
            self.ui.pushButton_Pause.setText("Resume")
        else:
            ix = self.ui.listView_matchingRule.model().index(val['searchResult']['currentMatchingRuleObjectIndex'], 0)
            self.ui.listView_matchingRule.setCurrentIndex(ix)
            line = QStandardItem('[' + val['searchResult']['title'] + '] ---- [' + val['searchResult']['description'] + '] ---- ['+val['searchResult']['googleResult'])
            self.listView_ResultModel.appendRow(line)
            self.ui.lineEdit_submitCount.setText(str(val['submitCount']))
        #if val['searchResult']['currentMatchingRuleObjectIndex'] == len(self.MatchingRuleObjectList) - 1:
        #    self.ui.pushButton_Start.setEnabled(True)

    def LoadFileByLine(self, fileName):
        if os.path.exists(fileName):
            with open(fileName, "r") as f:
                array = f.readlines()
            return array

    def checkBox_isChecked(self):
        if self.ui.checkBox_ProxyEnable.isChecked():
            self.ui.groupBox_Proxy.setEnabled(True)
        else:
            self.ui.groupBox_Proxy.setEnabled(False)

    '''def MakelistViewLoad(self, fileName, flag):
        def listViewLoad():
            mode = QStandardItemModel()
            array = self.LoadFileByLine(fileName)
            if array is not None:
                self.KeywordList = array
                for Line in array:
                    Line = QStandardItem(Line)
                    mode.appendRow(Line)
                if flag == "KeywordListPath":
                    self.ui.lineEdit_KeywordListPath.setText(fileName)
                    self.ui.listView_Keyword.setModel(mode)
                    # self.ui.progressBar.setMaximum(len(array))

        return listViewLoad()'''

    def openFileNameDialog(self, flag):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Support Files (*.txt *.json);;All Files (*);;Python Files (*.py)",
                                                  options=options)
        if fileName:
            if flag == "KeywordListPath":
                self.MakelistViewLoad(fileName, flag)

    def selectFolderDialog(self, flag):
        root = Tk()
        root.withdraw()  # hide root
        self.queueRulePath = askdirectory(parent=root, initialdir=os.path.dirname(os.path.abspath(__file__)),title='Select Folder') # shows dialog box and return the path
        if flag == 'queueRulePath':
            self.ui.lineEdit_queueRulePath.setText(self.queueRulePath)

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
