from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow, QSizePolicy, QWidget, QTableWidgetItem, \
    QDesktopWidget, QScrollBar
from PyQt5.QtWidgets import QFileDialog

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QStringListModel, Qt
from MappDatFile import Ui_MainWindow
import sys
import os
import csv
import numpy as np
import time

from natsort import ns, natsorted

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Qt5Agg")

global figplot



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
        self.devpos = []
        self.devthick = []
        self.keys = []
        self.progress = 100
        self.progressBar.setValue(self.progress)
        self.labelMsg.setText('请选择一个文件夹 \n 注意：确认数据是由MPBrd.exe保存的txt数据！')
        self.labmsgoldtext = []
        self.mergdatas = []
        self.fig = 0
        self.scalek = 0.01
        self.lineFactor.setText(f"{self.scalek}")
        self.lineFactor.textChanged.connect(self.scalekchanged)
        #####################
        self.cutlowfrq = 2000
        self.labelFrq.setText('cutoff frequence is %dHz' % self.cutlowfrq)
        self.horizontalSlider.setValue(int(self.cutlowfrq / 20 - 1))
        #######################################################
        self.FileList.doubleClicked.connect(self.check_Item)
        #######################################################
        self.actionFold.triggered.connect(self.dirlistfile)
        #######################################################
        self.actionMergeFileView.triggered.connect(self.readmergfile)
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
        self.tempFilePath = 'F:/00_PRO/04_FCD/04_SMIF/300LP/MPBRD/mapping_data'
        self.folderPath = ''


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
            self.devpos = []
            self.devthick = []
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
        filepath = self.filepath
        if filepath != '':
            self.filepath = filepath
            filemid,filearea,fileret,fileB,fileC = self.collectMergDat(self.filepath)
            if len(filemid)>2 and len(filearea)>2 and len(fileret)>2:
                    self.hdat1 = []
                    self.hdat2 = []
                    self.hdat3 = []
                    self.devpos = []
                    self.devthick = []
                    self.keys = []
                    ########################################################################## read middle file
                    filemid = filepath + '/' + filemid
                    with open(filemid) as f:
                        f_csv = csv.reader(f)
                        headers = next(f_csv)
                        for i, rows in enumerate(f_csv):
                            self.hdat1.append(dict(zip(tuple(headers),tuple([int(string) for string in rows]))))
                    self.keys = headers
                    ########################################################################## read area file
                    filearea = filepath + '/' + filearea
                    with open(filearea) as f:
                        f_csv = csv.reader(f)
                        headers = next(f_csv)
                        for i, rows in enumerate(f_csv):
                            self.hdat2.append(dict(zip(tuple(headers),tuple([int(string) for string in rows]))))
                    ########################################################################## read result file
                    fileret = filepath + '/' + fileret
                    with open(fileret) as f:
                        f_csv = csv.reader(f)
                        headers = next(f_csv)
                        for i, rows in enumerate(f_csv):
                            self.hdat3.append(dict(zip(tuple(headers),tuple(rows))))
                    ########################################################################## read result file
                    fileret = filepath + '/' + fileB
                    with open(fileret) as f:
                        f_csv = csv.reader(f)
                        headers = next(f_csv)
                        for i, rows in enumerate(f_csv):
                            self.devpos.append(dict(zip(tuple(headers),tuple([int(string) for string in rows]))))
                    ########################################################################## read result file
                    fileret = filepath + '/' + fileC
                    with open(fileret) as f:
                        f_csv = csv.reader(f)
                        headers = next(f_csv)
                        for i, rows in enumerate(f_csv):
                            self.devthick.append(dict(zip(tuple(headers),tuple([int(string) for string in rows]))))
                    ########################################################################## display data
                          
                    # reset Size
                    self.resetSize(5+4,len(self.keys)+3)
                    kydev = ('max','mid','min')
                    # set rowtitles
                    self.setRowTitle(0,"pos")
                    self.setRowTitle(1,"Thick")
                    self.setRowTitle(2,"ret")
                    self.setRowTitle(3,"△Pos")
                    self.setRowTitle(4,"△Thick")
                    # ‘P E C D’
                    self.setRowTitle(5,"P")
                    self.setRowTitle(6,"E")
                    self.setRowTitle(7,"C")
                    self.setRowTitle(8,"D")

                    #################################################################################
                    # set collum title
                    line = 0
                    for item in self.keys:
                        self.setVerTitle(line,item)
                        line = line + 1
                    # set cell value row 0
                    line = 0
                    for item in self.keys:
                        val = self.getallkeyValue(item,self.hdat1)
                        self.setCellValue(line,3,round(np.ptp(val)*self.scalek,3))
                        line = line + 1
                    ########### 打印和中值最大的偏差 pos偏差
                    val1 = self.getallkeyValue('max',self.devpos)
                    val2 = self.getallkeyValue('mid',self.devpos)
                    val3 = np.subtract(val1,val2)
                    self.setCellValue(line,3,round(np.max(val3)*self.scalek,3))
                    # set cell value row 1
                    line = 0
                    for item in self.keys:
                        val = self.getallkeyValue(item,self.hdat2)
                        self.setCellValue(line,4,round(np.ptp(val)*self.scalek,3))
                        line = line + 1
                    ########### 打印和中值最大的偏差 pos偏差
                    val1 = self.getallkeyValue('max',self.devthick)
                    val2 = self.getallkeyValue('mid',self.devthick)
                    val3 = np.subtract(val1,val2)
                    self.setCellValue(line,4,round(np.max(val3)*self.scalek,3))
                    # set cell value row 5/6/7/8 - P E C D
                    line = 0
                    for item in self.keys:
                        val = self.getallkeyValue(item,self.hdat3)
                        pPercent = ( val.count('P') * 100.0 / len(self.hdat3))
                        ePercent = ( val.count('E') * 100.0 / len(self.hdat3))
                        cPercent = ( val.count('C') * 100.0 / len(self.hdat3))
                        dPercent = ( val.count('D') * 100.0 / len(self.hdat3))
                        # print(len(self.hdat3))
                        self.setCellValue(line,5,round(pPercent,5))
                        self.setCellValue(line,6,round(ePercent,5))
                        self.setCellValue(line,7,round(cPercent,5))
                        self.setCellValue(line,8,round(dPercent,5))
                        line = line + 1
                    self.decodefinish = 1
                    plt.close("all")
                                                                                                               

    def maincyctask(self):
        self.timeStamp += 1
        if self.decode == 1:
            self.decodefinish = 0
            for i in range(self.startfle, self.endfle):
                # -------------
                self.progress = (i + 1) * 100 / self.filenum
                self.progressBar.setValue(int(self.progress))
                self.statusbar.showMessage(self.FilListStr[i])
                # -------------
                strpathfile = self.filepath + '/' + self.FilListStr[i]
                numSlot,objmid,objarea,objresult,devmid,devarea = self.readStdOfOneFile(strpathfile)
                # 取数据
                self.hdat1.append(objmid)
                self.hdat2.append(objarea)
                self.hdat3.append(objresult)
                self.devpos.append(devmid)
                self.devthick.append(devarea)

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
                self.resetSize(5 + 4,len(self.keys) + 3)
                # set rowtitles
                self.setRowTitle(0,"pos")
                self.setRowTitle(1,"Thick")
                self.setRowTitle(2,"ret")
                self.setRowTitle(3,"△Pos")
                self.setRowTitle(4,"△Thick")
                # ‘P E C D’
                self.setRowTitle(5,"P")
                self.setRowTitle(6,"E")
                self.setRowTitle(7,"C")
                self.setRowTitle(8,"D")

                kydev = ('max','mid','min')
                #################################################################################
                # set collum title
                line = 0
                for item in self.keys:
                    self.setVerTitle(line,item)
                    line = line + 1
                for item in kydev:
                    self.setVerTitle(line,item)
                    line = line + 1
                # set cell value row 3
                line = 0
                valist0 = []
                for item in self.keys:
                    val = self.getallkeyValue(item,self.hdat1)
                    self.setCellValue(line,3,round(np.ptp(val)*self.scalek,3))
                    valist0.append(np.ptp(val))
                    line = line + 1
                ########### 打印和中值最大的偏差 pos偏差
                val1 = self.getallkeyValue('max',self.devpos)
                val2 = self.getallkeyValue('mid',self.devpos)
                val3 = np.subtract(val1,val2)
                self.setCellValue(line,3,round(np.max(val3)*self.scalek,3))

                # set cell value row 4
                line = 0
                valist = []
                for item in self.keys:
                    val = self.getallkeyValue(item,self.hdat2)
                    self.setCellValue(line,4,round(np.ptp(val)*self.scalek,3))
                    valist.append(np.ptp(val))
                    line = line + 1
                ########### 打印和中值最大的偏差 thick偏差
                val1 = self.getallkeyValue('max',self.devthick)
                val2 = self.getallkeyValue('mid',self.devthick)
                val3 = np.subtract(val1,val2)
                self.setCellValue(line,4,round(np.max(val3)*self.scalek,3))

                # set cell value row 5/6/7/8 -P E C D
                line = 0
                valist = []
                for item in self.keys:
                    val = self.getallkeyValue(item,self.hdat3)
                    # print(val)
                    pPercent = ( val.count('P') * 100.0 / len(self.hdat3))
                    ePercent = ( val.count('E') * 100.0 / len(self.hdat3))
                    cPercent = ( val.count('C') * 100.0 / len(self.hdat3))
                    dPercent = ( val.count('D') * 100.0 / len(self.hdat3))
                    # print(len(self.hdat3))
                    self.setCellValue(line,5,round(pPercent,5))
                    self.setCellValue(line,6,round(ePercent,5))
                    self.setCellValue(line,7,round(cPercent,5))
                    self.setCellValue(line,8,round(dPercent,5))
                    line = line + 1

                #################################################################################
                # ----get time MergDat_B_230305_192702.csv
                times = time.strftime('%y%m%d_%H%M%S', time.localtime(time.time()))
                with open(self.filepath + '/' + 'MergDat_B_' + str(times) + '.csv', 'w', encoding='utf-8', newline='') as \
                        file_obj:
                    writer = csv.writer(file_obj)
                    writer.writerow(kydev)
                    for p in self.devpos:
                        writer.writerow(list(p.values()))
                
                 # ----get time MergDat_C_230305_192702.csv
                times = time.strftime('%y%m%d_%H%M%S', time.localtime(time.time()))
                with open(self.filepath + '/' + 'MergDat_C_' + str(times) + '.csv', 'w', encoding='utf-8', newline='') as \
                        file_obj:
                    writer = csv.writer(file_obj)
                    writer.writerow(kydev)
                    for p in self.devthick:
                        writer.writerow(list(p.values()))

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
                # ----get time MergDat_MIDDLE_230305_192702.csv
                times = time.strftime('%y%m%d_%H%M%S', time.localtime(time.time()))
                with open(self.filepath + '/' + 'MergDat_MIDDLE_' + str(times) + '.csv', 'w', encoding='utf-8', newline='') as \
                        file_obj:
                    writer = csv.writer(file_obj)
                    writer.writerow(self.keys)
                    for p in self.hdat1:
                        writer.writerow(list(p.values()))
                    # writer.writerow(valist0)
                # ----get time MergDat_AREA_230305_192702.csv
                times = time.strftime('%y%m%d_%H%M%S', time.localtime(time.time()))
                with open(self.filepath + '/' + 'MergDat_AREA_' + str(times) + '.csv', 'w', encoding='utf-8', newline='') as \
                        file_obj:
                    writer = csv.writer(file_obj)
                    writer.writerow(self.keys)
                    for p in self.hdat2:
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
                if(index.row()<len(self.keys)):
                    val = self.getallkeyValue(self.keys[index.row()],self.hdat1)
                    self.plotdats((val),len(val),0)
                else:
                    val1=self.getallkeyValue('max',self.devpos)
                    val2=self.getallkeyValue('mid',self.devpos)
                    val3=self.getallkeyValue('min',self.devpos)
                    self.plot3dats(val1,val2,val3,len(val1),0)
                    ########### 打印和中值最大的偏差 pos偏差
                    val1 = self.getallkeyValue('max',self.devpos)
                    val2 = self.getallkeyValue('mid',self.devpos)
                    val3 = np.subtract(val1,val2)
                    self.plotdats((val3),len(val3),1)
                    
            if(index.column()==4):
                if(index.row()<len(self.keys)):
                    val = self.getallkeyValue(self.keys[index.row()],self.hdat2)
                    self.plotdats((val),len(val),1)
                else:
                    val1=self.getallkeyValue('max',self.devthick)
                    val2=self.getallkeyValue('mid',self.devthick)
                    val3=self.getallkeyValue('min',self.devthick)
                    self.plot3dats(val1,val2,val3,len(val1),0)
                    ########### 打印和中值最大的偏差 pos偏差
                    val1 = self.getallkeyValue('max',self.devthick)
                    val2 = self.getallkeyValue('mid',self.devthick)
                    val3 = np.subtract(val1,val2)
                    self.plotdats((val3),len(val3),1)

    def getallkeyValue(self,key,dat):
        val = []
        for item in dat:
            val.append(item[key])
        return val
    

    def plot3dats(self,val1,val2,val3,num,pos):
        # plot method
        # ---< ,set plot space
        fig, ax = plt.subplots()
        agx = QDesktopWidget().availableGeometry()
        xx = agx.width() / 2 - (self.width() + 800) / 2
        yy = agx.height() / 2 - self.height() / 2 - 31
        plt.get_current_fig_manager().window.setGeometry(xx + self.width() + 5, yy + 31 + pos * 300, 800, 300)
        # ---< ,plot data
        plt.plot([i for i in range(num)], val1, 'm-x')
        plt.plot([i for i in range(num)], val2, 'k-x')
        plt.plot([i for i in range(num)], val3, 'c-x')
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
        plt.plot([i for i in range(num)], val, 'y-x')
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
        filepath = QFileDialog.getExistingDirectory()
        # filepath = self.tempFilePath
        if filepath != '':
            self.filepath = filepath
            self.FilListStr = self.collectfilstr(self.filepath)
            self.filenum = len(self.FilListStr)
            self.mergdatas = []

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
            if strFilename == 'MergDat_B':
                fileB = file_name
            if strFilename == 'MergDat_C':
                fileC = file_name
        ##########################################################################
        return filemiddle,filearea,fileresult,fileB,fileC

    # ----------------------------------------analyse the data of the single file and plot the curve
    def analySingleFile(self, filepath):
        numSlot,objmid,objarea,objresult,devmid,devarea = self.readStdOfOneFile(filepath)
        keys = objmid.keys()
        # reset Size
        self.resetSize(5+4 , numSlot + 3)
        # set rowtitles
        self.setRowTitle(0,"pos")
        self.setRowTitle(1,"Thick")
        self.setRowTitle(2,"ret")
        self.setRowTitle(3,"△Pos")
        self.setRowTitle(4,"△Thick")
        # ‘P E C D’
        self.setRowTitle(5,"P")
        self.setRowTitle(6,"E")
        self.setRowTitle(7,"C")
        self.setRowTitle(8,"D")
        # set collum title
        line = 0
        for item in keys:
            self.setVerTitle(line,item)
            line = line + 1
        for item in devmid:
            self.setVerTitle(line,item)
            line = line + 1
        # set cell value row 0
        line = 0
        for item in objmid:
            # print(objarea[item])
            self.setCellValue(line,0,round(objmid[item]*self.scalek,3))
            line = line + 1
        for item in devmid:
            self.setCellValue(line,0,round(devmid[item]*self.scalek,3))
            line = line + 1
        # set cell value row 1
        line = 0
        for item in objarea:
            # print(objarea[item])
            self.setCellValue(line,1,round(objarea[item]*self.scalek,3))
            line = line + 1
        for item in devarea:
            self.setCellValue(line,1,round(devarea[item]*self.scalek,3))
            line = line + 1
        # set cell value row 1
        line = 0
        for item in objresult:
            # print(objarea[item])
            self.setCellValue(line,2,objresult[item])
            line = line + 1

    # ----------------------------------------function to read std out of one single file
    def readStdOfOneFile(self, filepath):
        with open(filepath) as f:
            rawcontent = f.read()
            objmid={}
            objarea={}
            objresult={}

            kydev = ('max','mid','min')
            devmid = dict.fromkeys(kydev)
            devarea = dict.fromkeys(kydev)

            content = rawcontent.replace(" ", "")
            try:
                numSlot = int(content.split('numSlots:')[1].split('\n')[0]);
            except:
                print("no numSlot1")
            
            try:
                numSlot = int(content.split('slotNum:')[1].split('\n')[0]);
            except:
                print("no numSlot2")
                
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
            ########################
            b = list(objmid.values())
            a = np.sort([ x for x in b if x > 0 ])
            devmid['max'] = np.max(a)
            devmid['min'] = np.min(a)
            devmid['mid'] = (a[int(len(a)/2)])
            ########################
            b = list(objarea.values())
            a = np.sort([ x for x in b if x > 0 ])
            devarea['max'] = np.max(a)
            devarea['min'] = np.min(a)
            devarea['mid'] = (a[int(len(a)/2)])
            ########################
            return numSlot,objmid,objarea,objresult,devmid,devarea
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
    x = int(ag.width() / 2 - (mainWindow.width() + 800) / 2)
    y = int(ag.height() / 2 - mainWindow.height() / 2 - 31)
    #######################################################
    #mainWindow.move(x, y)
    mainWindow.show()
    #######################################################
    #figplot = plt.subplots()
    #plt.get_current_fig_manager().window.setGeometry(x + mainWindow.width() + 5, y + 31, 800, 514)
    #plt.show(block=False)
    #######################################################
    sys.exit(app.exec_())
