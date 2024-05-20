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

        self.changeCmos = QAction(QIcon("./Bitmap/symimportant.gif"), '切换', self)

        self.recordDat = QAction(QIcon("./Bitmap/symparam.gif"), '记录数据', self)
        self.showDat = QAction(QIcon("./Bitmap/symeffect.gif"), '停止并显示', self)
        

        self.toolBar = self.addToolBar('串口链接')
        self.toolBar.addAction(self.search)
        self.toolBar.addSeparator()
        self.toolBar.addWidget(self.cmbComlist)
        self.toolBar.addSeparator()
        self.toolBar.addWidget(self.cmbBrdrate)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.connect)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.disconnect)

        self.toolBar2 = QToolBar()
        self.addToolBar(QtCore.Qt.BottomToolBarArea,self.toolBar2)
        self.toolBar2.addAction(self.changeCmos)
        self.toolBar2.addSeparator()
        self.toolBar2.addAction(self.recordDat)
        self.toolBar2.addAction(self.showDat)
        ###################################################------------------------------------ Modbus Table
        tabRows = 10 #systempara numbers need to display
        tabCols = 2
        self.SysParatable = QtWidgets.QTableWidget(self.centralwidget)
        self.SysParatable.setGeometry(QtCore.QRect(0, 0, 400, 327))
        self.SysParatable.setObjectName("SysParatable")
        self.SysParatable.setColumnCount(tabCols)
        self.SysParatable.setRowCount(tabRows)

        for i in range(0,tabRows):
            item = QtWidgets.QTableWidgetItem()
            self.SysParatable.setVerticalHeaderItem(i, item)

        # self.SysParatable.setCellWidget(60-1, 0, self.cmbETYPE)
        ###################################################
        item = QtWidgets.QTableWidgetItem()
        self.SysParatable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.SysParatable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.SysParatable.setHorizontalHeaderItem(2, item)

        self.SysParatable.horizontalHeader().setDefaultSectionSize(70)
        self.SysParatable.horizontalHeader().setMinimumSectionSize(20)
        self.setVerTitle(0,'CMOS_POS')
        self.setVerTitle(1,'ENC_POS')
        self.setVerTitle(2,'SELECT')
        self.setVerTitle(3,'CHECK')
        self.setVerTitle(4,'设备ID')
        self.setVerTitle(5,'.二值化阈值')
        self.setVerTitle(6,'Wafer PST')
        self.setVerTitle(7,'Output enable')
        self.setVerTitle(8,'CMOS温度')
        self.setVerTitle(9,'Reserve')

        self.setRowTitle(0,'ActValue')
        self.setRowTitle(1,'Descript')

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


    def setVerTitle(self, index, verStr):
        _translate = QtCore.QCoreApplication.translate
        item = self.SysParatable.verticalHeaderItem(index)
        item.setText(_translate("MainWindow", verStr))

    
    def setRowTitle(self, index, verStr):
        _translate = QtCore.QCoreApplication.translate
        item = self.SysParatable.horizontalHeaderItem(index)
        item.setText(_translate("MainWindow", verStr))

    def resetSize(self, col, row):
        self.SysParatable.setColumnCount(col)
        self.SysParatable.setRowCount(row)
        for i in range(0,row):
            item = QtWidgets.QTableWidgetItem()
            self.SysParatable.setVerticalHeaderItem(i, item)
        for i in range(0,col):
            item = QtWidgets.QTableWidgetItem()
            self.SysParatable.setHorizontalHeaderItem(i, item)

    def setCellValue(self,col,row,value):
        self.SysParatable.setItem(col, row, QtWidgets.QTableWidgetItem(str(value)))
