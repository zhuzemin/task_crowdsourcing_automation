# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(230, 10, 551, 461))
        self.groupBox_2.setObjectName("groupBox_2")
        self.listView_Result = QtWidgets.QListView(self.groupBox_2)
        self.listView_Result.setGeometry(QtCore.QRect(10, 60, 531, 391))
        self.listView_Result.setObjectName("listView_Result")
        self.pushButton_SaveToDB = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_SaveToDB.setEnabled(True)
        self.pushButton_SaveToDB.setGeometry(QtCore.QRect(480, 20, 65, 21))
        self.pushButton_SaveToDB.setObjectName("pushButton_SaveToDB")
        self.progressBar = QtWidgets.QProgressBar(self.groupBox_2)
        self.progressBar.setGeometry(QtCore.QRect(10, 20, 461, 21))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(10, 20, 81, 16))
        self.label.setObjectName("label")
        self.lineEdit_submitCount = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_submitCount.setGeometry(QtCore.QRect(110, 20, 31, 20))
        self.lineEdit_submitCount.setObjectName("lineEdit_submitCount")
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_4.setGeometry(QtCore.QRect(170, 0, 181, 51))
        self.groupBox_4.setObjectName("groupBox_4")
        self.checkBox_debugEnable = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_debugEnable.setGeometry(QtCore.QRect(10, 10, 81, 16))
        self.checkBox_debugEnable.setObjectName("checkBox_debugEnable")
        self.label_2 = QtWidgets.QLabel(self.groupBox_4)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 91, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit_stepInterval = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_stepInterval.setGeometry(QtCore.QRect(100, 30, 31, 20))
        self.lineEdit_stepInterval.setObjectName("lineEdit_stepInterval")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 10, 191, 461))
        self.groupBox_3.setObjectName("groupBox_3")
        self.listView_matchingRule = QtWidgets.QListView(self.groupBox_3)
        self.listView_matchingRule.setGeometry(QtCore.QRect(10, 60, 171, 391))
        self.listView_matchingRule.setObjectName("listView_matchingRule")
        self.pushButton_queueRuleBrowser = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_queueRuleBrowser.setGeometry(QtCore.QRect(130, 20, 51, 21))
        self.pushButton_queueRuleBrowser.setObjectName("pushButton_queueRuleBrowser")
        self.lineEdit_queueRulePath = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_queueRulePath.setGeometry(QtCore.QRect(10, 20, 111, 21))
        self.lineEdit_queueRulePath.setObjectName("lineEdit_queueRulePath")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 480, 191, 61))
        self.groupBox.setObjectName("groupBox")
        self.pushButton_Cancel = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_Cancel.setGeometry(QtCore.QRect(130, 20, 51, 23))
        self.pushButton_Cancel.setObjectName("pushButton_Cancel")
        self.pushButton_Start = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_Start.setGeometry(QtCore.QRect(10, 20, 51, 23))
        self.pushButton_Start.setObjectName("pushButton_Start")
        self.pushButton_Pause = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_Pause.setGeometry(QtCore.QRect(70, 20, 51, 23))
        self.pushButton_Pause.setObjectName("pushButton_Pause")
        self.groupBox_Proxy = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Proxy.setGeometry(QtCore.QRect(230, 480, 551, 61))
        self.groupBox_Proxy.setObjectName("groupBox_Proxy")
        self.radioButton_ProxyTypeSocks5 = QtWidgets.QRadioButton(self.groupBox_Proxy)
        self.radioButton_ProxyTypeSocks5.setGeometry(QtCore.QRect(480, 30, 61, 16))
        self.radioButton_ProxyTypeSocks5.setObjectName("radioButton_ProxyTypeSocks5")
        self.label_22 = QtWidgets.QLabel(self.groupBox_Proxy)
        self.label_22.setGeometry(QtCore.QRect(420, 10, 71, 16))
        self.label_22.setObjectName("label_22")
        self.radioButton_ProxyTypeHttp = QtWidgets.QRadioButton(self.groupBox_Proxy)
        self.radioButton_ProxyTypeHttp.setGeometry(QtCore.QRect(420, 30, 51, 16))
        self.radioButton_ProxyTypeHttp.setObjectName("radioButton_ProxyTypeHttp")
        self.checkBox_ProxyEnable = QtWidgets.QCheckBox(self.groupBox_Proxy)
        self.checkBox_ProxyEnable.setGeometry(QtCore.QRect(10, 30, 91, 16))
        self.checkBox_ProxyEnable.setObjectName("checkBox_ProxyEnable")
        self.lineEdit_Proxy = QtWidgets.QLineEdit(self.groupBox_Proxy)
        self.lineEdit_Proxy.setGeometry(QtCore.QRect(100, 20, 301, 31))
        self.lineEdit_Proxy.setObjectName("lineEdit_Proxy")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Crawler"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Result"))
        self.pushButton_SaveToDB.setText(_translate("MainWindow", "SaveToDB"))
        self.label.setText(_translate("MainWindow", "submitCount: "))
        self.groupBox_4.setTitle(_translate("MainWindow", "Debug"))
        self.checkBox_debugEnable.setText(_translate("MainWindow", "debugEnable"))
        self.label_2.setText(_translate("MainWindow", "stepInterval: "))
        self.groupBox_3.setTitle(_translate("MainWindow", "queueRule"))
        self.pushButton_queueRuleBrowser.setText(_translate("MainWindow", "Browser"))
        self.groupBox.setTitle(_translate("MainWindow", "Control"))
        self.pushButton_Cancel.setText(_translate("MainWindow", "Cancel"))
        self.pushButton_Start.setText(_translate("MainWindow", "Start"))
        self.pushButton_Pause.setText(_translate("MainWindow", "Pause"))
        self.groupBox_Proxy.setTitle(_translate("MainWindow", "Proxy"))
        self.radioButton_ProxyTypeSocks5.setText(_translate("MainWindow", "Socks5"))
        self.label_22.setText(_translate("MainWindow", "ProxyType:"))
        self.radioButton_ProxyTypeHttp.setText(_translate("MainWindow", "Http"))
        self.checkBox_ProxyEnable.setText(_translate("MainWindow", "ProxyEnable"))
