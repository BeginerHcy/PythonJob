from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow, QSizePolicy, QWidget, QTableWidgetItem, \
    QDesktopWidget, QScrollBar
from PyQt5.QtWidgets import QFileDialog

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QStringListModel, Qt
from uWindows import Ui_MainWindow
import sys
import os
import csv
import numpy as np
import time

from natsort import ns, natsorted

import matplotlib
import matplotlib.pyplot as plt

import serial
import serial.tools.list_ports

from pymodbus.client import ModbusSerialClient

matplotlib.use("Qt5Agg")

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # 设置应用程序的窗口图标
        self.setWindowIcon(QIcon("./Resourse/icon.png"))
        #######################################################
        self.anlytime = 10
        #####################
        self.progress = 100
        #######################################################
        self.FileList.doubleClicked.connect(self.check_Item)
        #######################################################
        self.actionFold.triggered.connect(self.dirlistfile)
        #######################################################
        self.actionMergeFileView.triggered.connect(self.readmergfile)
        #######################################################
        self.actionMergeFileTo.triggered.connect(self.setmergecmd)
        #######################################################
        self.timer_main = QTimer(self)
        self.timer_main.timeout.connect(self.maincyctask)
        self.timer_main.start(50)  # ---1s deal 150 filse
        #######################################################
        #self.tempFilePath = 'F:/00_PRO/04_FCD/04_SMIF/300LP/MPBRD/mapping_data'
        self.tempFilePath = 'F:/00_PRO/04_FCD/04_SMIF/300LP/Aligner/aligner_tool_v1.0.2/align_data'
        self.folderPath = ''
        #######################################################
        # 串口无效
        self.ser = None
        # 刷新串口外设按钮
        self.search.triggered.connect(self.refresh)
        # 波特率修改
        self.cmbBrdrate.activated.connect(self.baud_modify)
        # 串口号修改
        self.cmbComlist.activated.connect(self.com_modify)
        # 打开串口
        self.connect.triggered.connect(self.comopen)
        # 关闭串口
        self.disconnect.triggered.connect(self.comclose)
        #######################################################

    def setmergecmd(self):
        plt.close("all")       
    
    def readmergfile(self):
        plt.close("all")
                                                                                                                          
    def maincyctask(self):
        if self.ser != None:
            response = self.ser.read_holding_registers(address=0, count=10, slave=1)
            if response.isError():
                print("读取失败：", response)
            else:
                print("保持寄存器的值：", response.registers)    


        plt.close("all")
    
    def showMsg(self):
        plt.close("all")

    # show curve of the select col
    def showDat(self,index):
        plt.close("all")
    

    def plot3dats(self,val1,val2,val3,num,pos):
        # plot method
        # ---< ,set plot space
        fig, ax = plt.subplots()
        agx = QDesktopWidget().availableGeometry()
        xx = agx.width() / 2 - (self.width() + 800) / 2
        yy = agx.height() / 2 - self.height() / 2 - 31
        plt.get_current_fig_manager().window.setGeometry(xx + self.width() + 5, yy + 31 + pos * 300, 800, 300)
        # ---< ,plot data
        plt.scatter([i for i in range(num)], val1, alpha=0.5, color='blue', linewidth=0, zorder=1)
        plt.scatter([i for i in range(num)], val2, alpha=0.5, color='red', linewidth=0, zorder=1)
        plt.scatter([i for i in range(num)], val3, alpha=0.5, color='black', linewidth=0, zorder=1)
        plt.grid()
        plt.show(block=False)

    def plot2dats(self,val1,val2,num,pos):
        # plot method
        # ---< ,set plot space
        fig, ax = plt.subplots()
        agx = QDesktopWidget().availableGeometry()
        xx = agx.width() / 2 - (self.width() + 800) / 2
        yy = agx.height() / 2 - self.height() / 2 - 31
        plt.get_current_fig_manager().window.setGeometry(xx + self.width() + 5, yy + 31 + pos * 300, 800, 300)
        # ---< ,plot data
        plt.scatter([i for i in range(num)], val1, alpha=0.5, color='blue', linewidth=0, zorder=1)
        plt.scatter([i for i in range(num)], val2, alpha=0.5, color='gray', linewidth=0, zorder=1)
        plt.grid()
        plt.show(block=False)

    def plotdats(self,val,num,pos):
        # plot method
        # ---< ,set plot space
        fig, ax = plt.subplots()
        agx = QDesktopWidget().availableGeometry()
        xx = agx.width() / 2 - (self.width() + 800) / 2
        yy = agx.height() / 2 - self.height() / 2 - 31
        plt.get_current_fig_manager().window.setGeometry(xx + self.width() + 5, yy + 31 + pos * 300, 800, 300)
        # ---< ,plot data
        plt.scatter([i for i in range(num)], val, alpha=0.5, color='blue', linewidth=0, zorder=1)
        plt.grid()
        plt.show(block=False)

    def plotxy(self,xval,val,pos):
        # plot method
        # ---< ,set plot space
        fig, ax = plt.subplots()
        agx = QDesktopWidget().availableGeometry()
        xx = agx.width() / 2 - (self.width() + 800) / 2
        yy = agx.height() / 2 - self.height() / 2 - 31
        plt.get_current_fig_manager().window.setGeometry(xx + self.width() + 5, yy + 31 + pos * 300, 800, 800)
        # ---< ,plot data
        plt.scatter(xval, val, alpha=0.5, color='black', linewidth=0, zorder=1)
        plt.grid()
        plt.show(block=False)

    def plot2xy(self,xval1,val1,xval2,val2,pos):
        # plot method
        # ---< ,set plot space
        fig, ax = plt.subplots()
        agx = QDesktopWidget().availableGeometry()
        xx = agx.width() / 2 - (self.width() + 800) / 2
        yy = agx.height() / 2 - self.height() / 2 - 31
        plt.get_current_fig_manager().window.setGeometry(xx + self.width() + 5, yy + 31 + pos * 300, 800, 800)
        # ---< ,plot data
        plt.scatter(xval1, val1, alpha=0.5, color='black', linewidth=0, zorder=1)
        plt.scatter(xval2, val2, alpha=0.5, color='blue', linewidth=0, zorder=1)
        plt.grid()
        plt.show(block=False)
            

    def closeEvent(self, e):
        plt.close('all')
        time.sleep(0.5)
        self.timer_main.stop()

    def changecutfrq(self):
        plt.close('all')

    # ---------------------------------------read the file list of the Directory
    def dirlistfile(self):
        filepath = QFileDialog.getExistingDirectory()
        #filepath = self.tempFilePath
        if filepath != '':
            self.filepath = filepath
            self.FilListStr = self.collectfilstr(self.filepath)
            self.filenum = len(self.FilListStr)


    def filtedFile(self,filterstr,path):
        path_list = os.listdir(path)
        print(path_list)
        path_list = [x for x in path_list if os.path.splitext(x)[1] == filterstr]
        return path_list
    # ---------------------------------------sub-fuction read sort file list
    def collectfilstr(self, pathstr):
        file_str_list = []
        timearr = []
        file_time_name_list = []
        self.filtimelist = []
        ##########################################################################
        path_list = os.listdir(pathstr)

        # path_list = sorted(path_list, key=lambda x: os.path.getmtime(os.path.join(pathstr, x)))
        path_list = natsorted(path_list,alg=ns.PATH)
        ##########################################################################
        for file_name in path_list:
            # print(os.path.getmtime(os.path.join(pathstr, file_name)), file_name)
            strFilename = file_name[0:7]
            if strFilename != 'MergDat':
                timefile = os.path.getmtime(pathstr + '/' + file_name)
                timearr.append(timefile)
                timefilestr = (datetime.fromtimestamp(int(timefile)))
                file_str_list.append(file_name)
                self.filtimelist.append(f"{timefilestr}")
                file_time_name_list.append(f"{timefilestr}" + '    ' + file_name)
        ##########################################################################
        list_mod1 = QStringListModel()
        list_mod1.setStringList(file_time_name_list)
        self.FileList.setModel(list_mod1)
        ##########################################################################
        strline0 = '最早:' + self.filtimelist[0] + ' ' + file_str_list[0] + '\n'
        strline1 = '最晚:' + self.filtimelist[len(self.filtimelist) - 1] + ' ' + file_str_list[
            len(self.filtimelist) - 1] + '\n'
        strline2 = '总共时长：' + f"{(timearr[len(self.filtimelist) - 1] - timearr[0]):.1f}" + '秒' + ' 共%d个记录文件\n' % len(
            self.filtimelist)
        strline3 = '平均间隔' + f"{((timearr[len(self.filtimelist) - 1] - timearr[0]) / len(self.filtimelist)):.1f}" + '秒记录一次\n'
        self.labmsgoldtext = strline0 + strline1 + strline2 + strline3
        #self.labelMsg.setText(self.labmsgoldtext)

        ##########################################################################
        return file_str_list
    

    def collectMergDat(self, pathstr):
        plt.close('all')

    # ----------------------------------------analyse the data of the single file and plot the curve
    def analySingleFile(self, filepath):
        plt.close('all')

    def showCircle(self,datsita,datr_dat):
        plt.close('all')

    def show2Circle(self,datsita1,datr_dat1,datsita2,datr_dat2):
        plt.close('all')

    # ----------------------------------------function to read std out of one single file
    def readStdOfOneFile(self, filepath):
        plt.close('all')

    # ----------------------------------------double click the file action
    def check_Item(self, index):
        plt.close('all')

    # -------------------------------------------------------------------------------- 
    # 刷新串口
    def refresh(self):
        # 查询可用的串口
        plist = list(serial.tools.list_ports.comports())
        if len(plist) <= 0:
            self.statusbar.showMessage('no com available!')
        else:
            # 把所有的可用的串口输出到comboBox中去
            self.cmbComlist.clear()
            for i in range(0, len(plist)):
                plist_0 = list(plist[i])
                self.cmbComlist.addItem(str(plist_0[0]))

    # 波特率修改
    def baud_modify(self):
        if self.ser != None:
            self.ser.baudrate = int(self.cmbBrdrate.currentText())

    # 串口号修改
    def com_modify(self):
        if self.ser != None:
            self.ser.port = self.cmbComlist.currentText()

    #打开串口
    def comopen(self):
        
        try:
            #self.ser = serial.Serial(self.cmbComlist.currentText(), int(self.cmbBrdrate.currentText()), timeout=0.2)
            self.ser = ModbusSerialClient(method='rtu', port=self.cmbComlist.currentText(), baudrate=int(self.cmbBrdrate.currentText()), timeout=2)
            self.ser.strict = False
            # param strict: Strict timing, 1.5 character between requests.
            self.comopened = 1
        except:
            QMessageBox.critical(self, 'com', '没有可用的串口或当前串口被占用')
            return None
        # 字符间隔超时时间设置
        #self.ser.interCharTimeout = 0.0001
        # 1ms的单位
        #self.timer.start(10)
        self.statusbar.showMessage('communication opened.')
        ###############Button status###############
        self.connect.setEnabled(False)
        self.disconnect.setEnabled(True)

    # 关闭串口
    def comclose(self):
        #self.timer.stop()
        self.cmdWrite=False
        self.comopened = 0
        try:
            self.ser.close()
        except:
            QMessageBox.critical(self, 'com', '关闭串口失败')
            return None

        self.ser = None
        self.statusbar.showMessage('communication closed.')
        ###############Button status###############
        self.connect.setEnabled(True)
        self.disconnect.setEnabled(False)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    #######################################################
    ag = QDesktopWidget().availableGeometry()
    x = ag.width() / 2 - (mainWindow.width() + 800) / 2
    y = ag.height() / 2 - mainWindow.height() / 2 - 31
    #######################################################
    mainWindow.move((int)(x), (int)(y))
    mainWindow.show()
    #######################################################
    sys.exit(app.exec_())
