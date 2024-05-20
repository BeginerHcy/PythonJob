# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FileList.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from PyQt5.QtWidgets import QAction,QToolBar,QTableWidgetItem
from PyQt5.QtGui import QFont,QIcon,QBrush,QColor


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        #MainWindow.resize(400, 600)
        MainWindow.setFixedSize(400,600)
        ###################################################------------------------------------
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        ###################################################------------------------------------
        self.FileList = QtWidgets.QListView(self.centralwidget)
        self.FileList.setGeometry(QtCore.QRect(0, 500, 400, 50))
        font = QtGui.QFont()
        font.setFamily("Arial Unicode")
        font.setPointSize(9)
        self.FileList.setFont(font)
        self.FileList.setFrameShadow(QtWidgets.QFrame.Plain)
        self.FileList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.FileList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.FileList.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.FileList.setObjectName("FileList")

        ###################################################------------------------------------
        self.FileList.raise_()

        MainWindow.setCentralWidget(self.centralwidget)
        ###################################################------------------------------------ statusBar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        ###################################################------------------------------------ menuarBar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 364, 23))
        self.menubar.setObjectName("menubar")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)

        self.actionFold = QtWidgets.QAction(MainWindow)
        self.actionFold.setObjectName("actionFold")

        self.actionMergeFileTo = QtWidgets.QAction(MainWindow)
        self.actionMergeFileTo.setObjectName("actionMergeFileTo")

        self.actionMergeFileView = QtWidgets.QAction(MainWindow)
        self.actionMergeFileView.setObjectName("actionMergeFileView")

        self.menuAbout.addAction(self.actionFold)
        self.menuAbout.addSeparator()

        self.menuAbout.addAction(self.actionMergeFileTo)
        self.menuAbout.addSeparator()

        self.menuAbout.addAction(self.actionMergeFileView)
        self.menubar.addAction(self.menuAbout.menuAction())
        ###################################################------------------------------------toolBar
        self.cmbComlist = QtWidgets.QComboBox()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbComlist.sizePolicy().hasHeightForWidth())
        self.cmbComlist.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        self.cmbComlist.setFont(font)
        self.cmbComlist.setObjectName("cmbComlist")
        self.cmbComlist.addItem("no..")

        self.cmbBrdrate = QtWidgets.QComboBox()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbBrdrate.sizePolicy().hasHeightForWidth())
        self.cmbBrdrate.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        self.cmbBrdrate.setFont(font)
        self.cmbBrdrate.setObjectName("cmbBrdrate")
        self.cmbBrdrate.addItem("9600")
        self.cmbBrdrate.addItem("19200")
        self.cmbBrdrate.addItem("38400")
        self.cmbBrdrate.addItem("115200")

        self.connect    = QAction(QIcon("./Bitmap/connect_established.png"),'链接',self)
        self.disconnect = QAction(QIcon("./Bitmap/connect_no.png"),'断开链接',  self)
        self.search     = QAction(QIcon("./Bitmap/refresh.gif"), '刷新串口', self)

        self.toolBar = self.addToolBar('串口链接')
        self.toolBar.addAction(self.search)
        self.toolBar.addWidget(self.cmbComlist)
        self.toolBar.addWidget(self.cmbBrdrate)
        self.toolBar.addAction(self.connect)
        self.toolBar.addAction(self.disconnect)

        ###################################################------------------------------------window retranslate ui
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AlignDatAnalyse"))
        self.menuAbout.setTitle(_translate("MainWindow", "文件"))
        self.actionFold.setText(_translate("MainWindow", "Select Folder"))
        self.actionMergeFileTo.setText(_translate("MainWindow", "MergeFileTo"))
        self.actionMergeFileView.setText(_translate("MainWindow", "MergeFileView"))



