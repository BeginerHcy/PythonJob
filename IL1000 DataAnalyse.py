from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow, QSizePolicy, QWidget, QTableWidgetItem, \
    QDesktopWidget, QScrollBar
from PyQt5.QtWidgets import QFileDialog

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QStringListModel, Qt
from FileList import Ui_MainWindow
import sys
import os
import csv
import numpy as np
from scipy.fftpack import fft
from scipy import signal
import time

from natsort import ns, natsorted

import matplotlib
import matplotlib.pyplot as plt
import re
matplotlib.use("Qt5Agg")

global figplot


def FFT(Fs, data):
    """
    对输入信号进行FFT
    :param Fs:  采样频率
    :param data:待FFT的序列
    :return:
    """
    L = len(data)  # 信号长度
    N = np.power(2, np.ceil(np.log2(L)))  # 下一个最近二次幂，也即N个点的FFT
    result = np.abs(fft(x=data, n=int(N))) / L * 2  # N点FFT
    axisFreq = np.arange(int(N / 2)) * Fs / N  # 频率坐标
    result = result[range(int(N / 2))]  # 因为图形对称，所以取一半
    return axisFreq, result


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # 设置应用程序的窗口图标
        self.setWindowIcon(QIcon("./Resourse/icon.png"))
        #######################################################
        self.FilListStr = []
        self.MergFilListStr = []
        self.filepath = []
        self.deadline = 4100
        self.numToREAD = 3000
        self.tintvl = 1000  # means 1000us
        self.timeStamp = 0
        self.filtimelist = []
        self.anlytime = 4  # ----analyse 3 second's data
        self.lineEdit.setText(f"{self.anlytime}")
        self.lineEdit.textChanged.connect(self.analytimechange)
        #####################
        self.filenum = 0
        self.startfle = 0
        self.endfle = 0
        self.fldealnumcyc = 200
        self.cyctime = 0
        self.decode = 0
        self.cyccnt = 0
        self.hdat1 = []
        self.hdat2 = []
        self.hdat3 = []
        self.keys = []
        self.progress = 100
        self.progressBar.setValue(self.progress)
        self.labelMsg.setText('请选择一个文件夹 \n 注意：确认数据是由IL1000系统自动保存的CSV数据！')
        self.labmsgoldtext = []
        self.mergdatas = []
        self.fig = 0
        self.scalek = 0.01
        self.lineFactor.setText(f"{self.scalek}")
        self.lineFactor.textChanged.connect(self.scalekchanged)
        #####################
        self.cutlowfrq = 2000
        self.labelFrq.setText('cutoff frequence is %dHz' % self.cutlowfrq)
        self.horizontalSlider.setValue((self.cutlowfrq / 20 - 1))
        #######################################################
        self.FileList.doubleClicked.connect(self.check_Item)
        #######################################################
        self.actionFold.triggered.connect(self.dirlistfile)
        #######################################################
        self.horizontalSlider.valueChanged.connect(self.changecutfrq)
        #######################################################
        self.actionMergeFileTo.triggered.connect(self.setmergecmd)
        #######################################################
        self.timer_main = QTimer(self)
        self.timer_main.timeout.connect(self.maincyctask)
        self.timer_main.start(1000)  # ---1s deal 150 filse
        #######################################################
        self.SysParatable.itemDoubleClicked.connect(self.showDat)
        #######################################################
        # self.setVerTitle( index=0, verStr="Slot0")
        # self.setColTitle( index=0, verStr="ObjMiddle")
        self.resetSize(1,1)
        self.setCellValue(0,0,"IDLE")
        self.decodefinish = 0


    def scalekchanged(self):
        if self.lineFactor.text() != '':
            self.scalek = float(self.lineFactor.text())

    def analytimechange(self):
        if self.lineEdit.text() != '':
            self.anlytime = float(self.lineEdit.text())

    def setmergecmd(self):
        if self.filenum > 0:
            self.startfle = 0
            # ------------------------------start decode command
            self.hdat1 = []
            self.hdat2 = []
            self.hdat3 = []
            self.keys = []
            self.decode = 1
            self.cyccnt = 0  # clear tag
            self.cyctime = int(np.ceil(self.filenum / self.fldealnumcyc))
            plt.close("all")
            # ------------------------------
            if self.cyctime > 1:
                self.endfle = self.fldealnumcyc
            else:
                self.endfle = self.filenum
            # ------------------------------
    
    def readmergfile(self):
        filepath = 'F:/00_PRO/04_FCD/04_SMIF/300LP/MPBRD/mapping_data'
        if filepath != '':
            self.filepath = filepath
            filemid,filearea,fileret = self.collectMergDat(self.filepath)
            if len(filemid)>2 and len(filearea)>2 and len(fileret)>2:
                
                                                                                                               

    def maincyctask(self):
        self.timeStamp += 1
        if self.decode == 1:
            self.decodefinish = 0
            for i in range(self.startfle, self.endfle):
                # -------------
                self.progress = (i + 1) * 100 / self.filenum
                self.progressBar.setValue(self.progress)
                self.statusbar.showMessage(self.FilListStr[i])
                # -------------
                strpathfile = self.filepath + '/' + self.FilListStr[i]
                numSlot,objmid,objarea,objresult = self.readStdOfOneFile(strpathfile)
                # 取数据
                self.hdat1.append(objmid)
                self.hdat2.append(objarea)
                self.hdat3.append(objresult)
                
                # plot method
                # ---< ,close all
                # plt.close("all")
                # ---< ,set plot space
                # fig, ax = plt.subplots()
                # agx = QDesktopWidget().availableGeometry()
                # xx = agx.width() / 2 - (self.width() + 800) / 2
                # yy = agx.height() / 2 - self.height() / 2 - 31
                # plt.get_current_fig_manager().window.setGeometry(xx + self.width() + 5, yy + 31 - 230, 800, 300)
                # ---< ,plot data
                # plt.plot(x, self.hdat1, 'm-*')
                # plt.plot(x, y1, 'c-')
                # plt.grid()
                # plt.show(block=False)
                
            # -------------
            self.cyccnt += 1
            # -------------
            if self.cyccnt >= self.cyctime:
                self.decode = 0
                plt.close("all")
                self.keys = list(objmid.keys())
                # val = self.getallkeyValue("slot12",self.hdat1)
                # self.plotdats(val,len(val))
                # reset Size
                self.resetSize(5,len(self.keys))
                # set rowtitles
                self.setRowTitle(0,"pos")
                self.setRowTitle(1,"Thick")
                self.setRowTitle(2,"ret")
                self.setRowTitle(3,"△Pos")
                self.setRowTitle(4,"△Thick")
                #################################################################################
                # set collum title
                line = 0
                for item in self.keys:
                    self.setVerTitle(line,item)
                    line = line + 1
                # set cell value row 0
                line = 0
                valist = []
                for item in self.keys:
                    val = self.getallkeyValue(item,self.hdat1)
                    self.setCellValue(line,3,round(np.ptp(val)*self.scalek,3))
                    valist.append(np.ptp(val))
                    line = line + 1
                # ----get time MergDat_MIDDLE_230305_192702.csv
                times = time.strftime('%y%m%d_%H%M%S', time.localtime(time.time()))
                with open(self.filepath + '/' + 'MergDat_MIDDLE_' + str(times) + '.csv', 'w', encoding='utf-8', newline='') as \
                        file_obj:
                    writer = csv.writer(file_obj)
                    writer.writerow(self.keys)
                    for p in self.hdat1:
                        writer.writerow(list(p.values()))
                    writer.writerow(valist)

                # set cell value row 1
                line = 0
                valist = []
                for item in self.keys:
                    val = self.getallkeyValue(item,self.hdat2)
                    self.setCellValue(line,4,round(np.ptp(val)*self.scalek,3))
                    valist.append(np.ptp(val))
                    line = line + 1
                # ----get time MergDat_AREA_230305_192702.csv
                times = time.strftime('%y%m%d_%H%M%S', time.localtime(time.time()))
                with open(self.filepath + '/' + 'MergDat_AREA_' + str(times) + '.csv', 'w', encoding='utf-8', newline='') as \
                        file_obj:
                    writer = csv.writer(file_obj)
                    writer.writerow(self.keys)
                    for p in self.hdat2:
                        writer.writerow(list(p.values()))
                    writer.writerow(valist)

                # set cell value row 2
                # ----get time MergDat_AREA_230305_192702.csv
                times = time.strftime('%y%m%d_%H%M%S', time.localtime(time.time()))
                with open(self.filepath + '/' + 'MergDat_RET_' + str(times) + '.csv', 'w', encoding='utf-8', newline='') as \
                        file_obj:
                    writer = csv.writer(file_obj)
                    writer.writerow(self.keys)
                    for p in self.hdat3:
                        writer.writerow(list(p.values()))
                    # writer.writerow(valist)
                self.decodefinish = 1
                #####################################################
            else:
                self.startfle = self.cyccnt * self.fldealnumcyc
                self.endfle = self.startfle + self.fldealnumcyc
                if self.endfle > self.filenum:
                    self.endfle = self.filenum
    
    # show curve of the select col
    def showDat(self,index):
        if(self.decodefinish == 1):
            if(index.column()==3):
                val = self.getallkeyValue(self.keys[index.row()],self.hdat1)
                self.plotdats((val),len(val),0)
            if(index.column()==4):
                val = self.getallkeyValue(self.keys[index.row()],self.hdat2)
                self.plotdats((val),len(val),1)

    def getallkeyValue(self,key,dat):
        val = []
        for item in dat:
            val.append(item[key])
        return val
    
    def plotdats(self,val,num,pos):
        # plot method
        # ---< ,set plot space
        fig, ax = plt.subplots()
        agx = QDesktopWidget().availableGeometry()
        xx = agx.width() / 2 - (self.width() + 800) / 2
        yy = agx.height() / 2 - self.height() / 2 - 31
        plt.get_current_fig_manager().window.setGeometry(xx + self.width() + 5, yy + 31 + pos * 300, 800, 300)
        # ---< ,plot data
        plt.plot([i for i in range(num)], val, 'm-*')
        plt.grid()
        plt.show(block=False)
            

    def closeEvent(self, e):
        plt.close('all')
        time.sleep(0.5)
        self.timer_main.stop()

    def changecutfrq(self):
        self.cutlowfrq = (1 + self.horizontalSlider.value()) * 20
        self.labelFrq.setText('cutoff frequence change to %dHz' % self.cutlowfrq)

    # ---------------------------------------read the file list of the Directory
    def dirlistfile(self):
        # filepath = QFileDialog.getExistingDirectory()

        filepath = 'F:/00_PRO/04_FCD/04_SMIF/300LP/MPBRD/mapping_data'
        if filepath != '':
            self.filepath = filepath
            self.FilListStr = self.collectfilstr(self.filepath)
            self.filenum = len(self.FilListStr)
            self.mergdatas = []

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
        self.labelMsg.setText(self.labmsgoldtext)

        ##########################################################################
        return file_str_list
    

    def collectMergDat(self, pathstr):

        ##########################################################################
        path_list = os.listdir(pathstr)

        # path_list = sorted(path_list, key=lambda x: os.path.getmtime(os.path.join(pathstr, x)))
        path_list = natsorted(path_list,alg=ns.PATH)
        ##########################################################################
        for file_name in path_list:
            # print(os.path.getmtime(os.path.join(pathstr, file_name)), file_name)
            strFilename = file_name[0:9]
            if strFilename == 'MergDat_M':
                filemiddle = file_name
            if strFilename == 'MergDat_A':
                filearea = file_name
            if strFilename == 'MergDat_R':
                fileresult = file_name
        ##########################################################################
        return filemiddle,filearea,fileresult

    # ----------------------------------------analyse the data of the single file and plot the curve
    def analySingleFile(self, filepath):
        numSlot,objmid,objarea,objresult = self.readStdOfOneFile(filepath)
        keys = objmid.keys()
        # reset Size
        self.resetSize(5,numSlot)
        # set rowtitles
        self.setRowTitle(0,"pos")
        self.setRowTitle(1,"Thick")
        self.setRowTitle(2,"ret")
        self.setRowTitle(3,"△Pos")
        self.setRowTitle(4,"△Thick")
        # set collum title
        line = 0
        for item in keys:
            self.setVerTitle(line,item)
            line = line + 1
        # set cell value row 0
        line = 0
        for item in objmid:
            # print(objarea[item])
            self.setCellValue(line,0,round(objmid[item]*self.scalek,3))
            line = line + 1
        # set cell value row 1
        line = 0
        for item in objarea:
            # print(objarea[item])
            self.setCellValue(line,1,round(objarea[item]*self.scalek,3))
            line = line + 1
        # set cell value row 1
        line = 0
        for item in objresult:
            # print(objarea[item])
            self.setCellValue(line,2,objresult[item])
            line = line + 1

    def filtdatabutter(self, datin):
        wn = self.cutlowfrq * 2 / (1000000 / self.tintvl)  # 10ms = 100Hz  2ms = 500Hz
        if wn < 0.9 and self.radioFile.isChecked():
            b, a = signal.butter(2, wn, 'low')
            data_flt = signal.filtfilt(b, a, datin)
        else:
            data_flt = datin
        return data_flt

    # ----------------------------------------function to read std out of one single file
    def readStdOfOneFile(self, filepath):
        with open(filepath) as f:
            rawcontent = f.read()
            objmid={}
            objarea={}
            objresult={}
            content = rawcontent.replace(" ", "")
            numSlot = int(content.split('numSlots:')[1].split('\n')[0])
            objmidContent = (content.split('objectMiddle:')[1].split('objectArea')[0]).split('\n')
            objareaContent = (content.split('objectArea:')[1].split('result')[0]).split('\n')
            objresultContent = (content.split('result:')[1]).split('\n')
            for item in objmidContent:
                if(len(item) > 0):
                    objmid[item.split(':')[0]] = int(item.split(':')[1])
            for item in objareaContent:
                if(len(item) > 0):
                    objarea[item.split(':')[0]] = int(item.split(':')[1])
            for item in objresultContent:
                if(len(item) > 0):
                    objresult[item.split(':')[0]] = item.split(':')[1]
            return numSlot,objmid,objarea,objresult
            ##########################################################################

    # ----------------------------------------double click the file action
    def check_Item(self, index):
        strPathFile = self.filepath + '/' + self.FilListStr[index.row()]
        self.analySingleFile(strPathFile)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    #######################################################
    ag = QDesktopWidget().availableGeometry()
    x = ag.width() / 2 - (mainWindow.width() + 800) / 2
    y = ag.height() / 2 - mainWindow.height() / 2 - 31
    #######################################################
    mainWindow.move(x, y)
    mainWindow.show()
    #######################################################
    figplot = plt.subplots()
    plt.get_current_fig_manager().window.setGeometry(x + mainWindow.width() + 5, y + 31, 800, 514)
    plt.show(block=False)
    #######################################################
    sys.exit(app.exec_())
