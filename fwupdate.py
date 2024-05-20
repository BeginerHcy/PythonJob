# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fwupdate.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from PyQt5.QtWidgets import QAction,QToolBar,QTableWidgetItem
from PyQt5.QtGui import QFont,QIcon,QBrush,QColor



class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 100)
       # MainWindow.setFixedSize(400,111)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 581, 51))



        self.cmbComlist = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbComlist.sizePolicy().hasHeightForWidth())
        self.cmbComlist.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        self.cmbComlist.setFont(font)
        self.cmbComlist.setObjectName("cmbComlist")
        self.cmbComlist.addItem("")
        self.cmbComlist.addItem("")
        self.cmbComlist.addItem("")


        self.cmbBrdrate = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbBrdrate.sizePolicy().hasHeightForWidth())
        self.cmbBrdrate.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        self.cmbBrdrate.setFont(font)
        self.cmbBrdrate.setObjectName("cmbBrdrate")
        self.cmbBrdrate.addItem("")
        self.cmbBrdrate.addItem("")
        self.cmbBrdrate.addItem("")
        self.cmbBrdrate.addItem("")

        eTypeNum = 18
        self.cmbETYPE = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        for i in range(0,eTypeNum):
            self.cmbETYPE.addItem("")



        self.BarWriteProcess    = QtWidgets.QProgressBar(self.centralwidget)
        self.BinFileLable       = QtWidgets.QLabel(self.centralwidget)


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)




        self.version    = QAction(QIcon("./Bitmap/symstatus.gif"),'Version',self)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&About')
        fileMenu.addAction(self.version)


        self.connect    = QAction(QIcon("./Bitmap/connect_established.png"),'链接',self)
        self.disconnect = QAction(QIcon("./Bitmap/connect_no.png"),'断开链接',  self)
        self.search     = QAction(QIcon("./Bitmap/refresh.gif"), '刷新串口', self)
        self.updateFirmware = QAction(QIcon("./Bitmap/firmware.png"), '更新固件', self)
        self.selBinfile = QAction(QIcon("./Bitmap/openfile.png"), '选择固件', self)
        self.readSysPara = QAction(QIcon("./Bitmap/symeffect.gif"), '读取参数', self)
        self.writeSysPara = QAction(QIcon("./Bitmap/symparam.gif"), '下载参数', self)

        tbar = self.addToolBar('链接设备')
        tbar.addAction(self.search)
        tbar.addWidget(self.cmbComlist)
        tbar.addWidget(self.cmbBrdrate)
        tbar.addAction(self.connect)
        tbar.addAction(self.disconnect)

        firmwareBar = QToolBar()
        self.addToolBar(QtCore.Qt.BottomToolBarArea,firmwareBar)
        firmwareBar.addAction(self.selBinfile)
        firmwareBar.addAction(self.updateFirmware)
        firmwareBar.addWidget(self.BarWriteProcess)
        firmwareBar.addWidget(self.BinFileLable)

        SystemparBar = self.addToolBar('更改参数')
        SystemparBar.addAction(self.readSysPara)
        SystemparBar.addAction(self.writeSysPara)

        tabRows = 61 #systempara numbers need to display
        tabCols = 2
        self.SysParatable = QtWidgets.QTableWidget(self.centralwidget)
        self.SysParatable.setGeometry(QtCore.QRect(0, 0, 400, 400))
        self.SysParatable.setObjectName("SysParatable")
        self.SysParatable.setColumnCount(tabCols)
        self.SysParatable.setRowCount(tabRows)
        ###################################################

        for i in range(0,tabRows):
            item = QtWidgets.QTableWidgetItem()
            self.SysParatable.setVerticalHeaderItem(i, item)

        self.SysParatable.setCellWidget(60-1, 0, self.cmbETYPE)
        ###################################################
        item = QtWidgets.QTableWidgetItem()
        self.SysParatable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.SysParatable.setHorizontalHeaderItem(1, item)

        self.SysParatable.horizontalHeader().setDefaultSectionSize(134)
        self.SysParatable.horizontalHeader().setMinimumSectionSize(25)


        self.btnMachine = QtWidgets.QPushButton(self.centralwidget)
        self.btnMachine.setGeometry(QtCore.QRect(0, 400, 400, 300))
        self.btnMachine.setIconSize(QtCore.QSize(400, 300))

        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./Bitmap/find.png"))
        self.btnMachine.setIcon(icon2)








        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FirmwareUpdateTool LF"))

        self.cmbComlist.setItemText(0, _translate("MainWindow", "Com1"))
        self.cmbComlist.setItemText(1, _translate("MainWindow", "Com2"))
        self.cmbComlist.setItemText(2, _translate("MainWindow", "Com3"))

        self.cmbBrdrate.setItemText(0, _translate("MainWindow", "9600"))
        self.cmbBrdrate.setItemText(1, _translate("MainWindow", "19200"))
        self.cmbBrdrate.setItemText(2, _translate("MainWindow", "38400"))
        self.cmbBrdrate.setItemText(3, _translate("MainWindow", "115200"))

        self.cmbETYPE.setItemText(0, _translate("MainWindow", "E1030"))
        self.cmbETYPE.setItemText(1, _translate("MainWindow", "E1090"))
        self.cmbETYPE.setItemText(2, _translate("MainWindow", "E2030"))
        self.cmbETYPE.setItemText(3, _translate("MainWindow", "E2030s"))
        self.cmbETYPE.setItemText(4, _translate("MainWindow", "E2090"))
        self.cmbETYPE.setItemText(5, _translate("MainWindow", "E2090s"))
        self.cmbETYPE.setItemText(6, _translate("MainWindow", "EH2030"))
        self.cmbETYPE.setItemText(7, _translate("MainWindow", "EH2030s"))
        self.cmbETYPE.setItemText(8, _translate("MainWindow", "EHJ2030"))
        self.cmbETYPE.setItemText(9, _translate("MainWindow", "EJ1090"))
        self.cmbETYPE.setItemText(10, _translate("MainWindow", "EH2090"))
        self.cmbETYPE.setItemText(11, _translate("MainWindow", "EH1030"))
        self.cmbETYPE.setItemText(12, _translate("MainWindow", "EH1090"))
        self.cmbETYPE.setItemText(13, _translate("MainWindow", "ERevers4"))
        self.cmbETYPE.setItemText(14, _translate("MainWindow", "F890_0710"))
        self.cmbETYPE.setItemText(15, _translate("MainWindow", "F890_0805"))
        self.cmbETYPE.setItemText(16, _translate("MainWindow", "F890_0808"))
        self.cmbETYPE.setItemText(17, _translate("MainWindow", "F890_1010"))

        self.BinFileLable.setText(_translate("MainWindow", "TextLabel"))
        self.btnMachine.setEnabled(False)
        self.SysParatable.setEnabled(False)
        ###################################################

        def setTabVerValue(self, index, verStr, unitStr):
            item = self.SysParatable.verticalHeaderItem(index)
            item.setText(_translate("MainWindow", verStr))
            self.SysParatable.setItem(index, 1, QTableWidgetItem(unitStr))
            return index + 1

        iVerHeader = 0
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="MeasurePosScale",unitStr="mm/unit")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="TargetExchScale",unitStr="1.0 unit")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="SynVelocity",unitStr="mm/s")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="BendX1",unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="BendH",unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="BackVel",unitStr="mm/s")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="FollowVelocity", unitStr="mm/s")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="MaualVelocity", unitStr="mm/s")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="ACC", unitStr="mm/s2")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="DEC", unitStr="mm/s2")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="StartPos", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="EndPos", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="BackPosition", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="OffsetPos", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="AutoBackPos", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="OffsetPos2", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="offsetBasic", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="offsetBasic_Teach", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="PosLimitSw", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="NegLimitSw", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="EnableSw", unitStr="ON=1")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="BendAngle", unitStr="°")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="BendPanX", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="PosLimitSw_B", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="NegLimitSw_B", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="ACC_B", unitStr="mm/s2")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="DEC_B", unitStr="mm/s2")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="MaualVelocity_B", unitStr="mm/s")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="BackPosition_B", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="BackVel_B", unitStr="mm/s")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="FollowVelocity_B", unitStr="mm/s")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="SynVelocity_B", unitStr="mm/s")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="Distance90Degree", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="AxisBScale", unitStr="1.0")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="TeachAngle", unitStr="°")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="EndPos_Teach", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="PositionOfstBR1", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="PositionOfstBR2", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="PositionOfstBR3", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="VmoldeD", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="VDistMachine", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="Vmolde2D", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="SpringH", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="MoldH", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="AngleScaleK", unitStr="1.0")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="EnableSim", unitStr="ON=1")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="MachineZeroOfset", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="Bend2TimeOfset", unitStr="second")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="AngleB", unitStr="°")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="PlatThick", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="HoldBendTime", unitStr="second")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="SuckDist", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="MachineZeroOfsetTemp", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="Pitch", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="Peri_meter", unitStr="mm")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="Ratios", unitStr="i:1")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="RevPulse", unitStr="pulse/rev")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="MachineType", unitStr="Up/Down")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="decLevel", unitStr="0:slow,1:normal,2:fast")
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="PayloadType", unitStr="Exxx /Fxxx")

        #############60 line
        iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="Firmware", unitStr="Y/M/D/n")


        #iVerHeader = setTabVerValue(self, index=iVerHeader, verStr="MachineCode", unitStr="string")


        ###################################################
        item = self.SysParatable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Value"))
        item = self.SysParatable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "units"))
        ###################################################
        for i in range(52,59):
            item = QtWidgets.QTableWidgetItem()
            item.setBackground(QBrush(QColor(255, 0, 0)))





