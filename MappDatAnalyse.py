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
        self.horizontalSlider.setValue((int)(self.cutlowfrq / 20 - 1))
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
        #self.tempFilePath = 'F:/00_PRO/04_FCD/04_SMIF/300LP/MPBRD/mapping_data'
        self.tempFilePath = 'F:/00_PRO/04_FCD/04_SMIF/300LP/Aligner/aligner_tool_v1.0.2/align_data'
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
            filemid = self.collectMergDat(self.filepath)
            if len(filemid)>2:
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
                            self.hdat1.append(float(rows[0]))
                            self.hdat2.append(float(rows[1]))
                            self.hdat3.append(float(rows[2]))
                            self.devpos.append(float(rows[3]))
                            self.devthick.append(float(rows[4]))

                            #print([int(string) for string in rows])
                            #self.hdat1.append(dict(zip(tuple(headers),tuple([int(string) for string in rows]))))
                        plt.close("all")
                        # val = self.getallkeyValue("slot12",self.hdat1)
                        # self.plotdats(val,len(val))
                        # reset Size
                        self.resetSize(5, len(self.hdat1))
                        # set rowtitles
                        self.setRowTitle(0,"X")
                        self.setRowTitle(1,"Y")
                        self.setRowTitle(2,"θ")
                        self.setRowTitle(3,"R")
                        self.setRowTitle(4,"△P")
                        #################################################################################
                        # set collum title
                        line = 0
                        for item in self.hdat1:
                            self.setVerTitle(line,str(line))
                            line = line + 1
                        # set cell value row 0
                        line = 0
                        for item in self.hdat1:
                            self.setCellValue(line,0,round(self.hdat1[line],3))
                            self.setCellValue(line,1,round(self.hdat2[line],3))
                            self.setCellValue(line,2,round(self.hdat3[line],3))
                            self.setCellValue(line,3,round(self.devpos[line],3))
                            self.setCellValue(line,4,round(self.devthick[line],3))
                            line = line + 1
                            
                        #self.plot2dats(self.hdat1, self.hdat2,len(self.hdat1),0)
                        #self.plotdats(self.devthick,len(self.devthick),0)
                        #self.plotdats(self.hdat3,len(self.devpos),0)
                        #self.plotxy(self.hdat1, self.hdat2, 0)
                    
                        self.showMsg()
                    ########################################################################## display data
                    
                                                                                                               

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
                numSlot,datsita,datr_dat,ret,strtime = self.readStdOfOneFile(strpathfile)
                # 取数据
                self.hdat1.append(ret[0])
                self.hdat2.append(ret[1])
                self.hdat3.append(ret[2])
                self.devpos.append(ret[3])
                self.devthick.append(np.sqrt(ret[0]*ret[0] + ret[1]*ret[1]))
                
            # -------------
            self.cyccnt += 1
            # -------------
            if self.cyccnt >= self.cyctime:
                self.decode = 0
                plt.close("all")
                # val = self.getallkeyValue("slot12",self.hdat1)
                # self.plotdats(val,len(val))
                # reset Size
                self.resetSize(5, len(self.hdat1))
                # set rowtitles
                self.setRowTitle(0,"X")
                self.setRowTitle(1,"Y")
                self.setRowTitle(2,"θ")
                self.setRowTitle(3,"R")
                self.setRowTitle(4,"△P")
                #################################################################################
                # set collum title
                line = 0
                for item in self.hdat1:
                    self.setVerTitle(line,str(line))
                    line = line + 1
                # set cell value row 0
                line = 0
                for item in self.hdat1:
                    self.setCellValue(line,0,round(self.hdat1[line],3))
                    self.setCellValue(line,1,round(self.hdat2[line],3))
                    self.setCellValue(line,2,round(self.hdat3[line],3))
                    self.setCellValue(line,3,round(self.devpos[line],3))
                    self.setCellValue(line,4,round(self.devthick[line],3))
                    line = line + 1

                #################################################################################
                # ----get time MergDat_B_230305_192702.csv
                times = time.strftime('%y%m%d_%H%M%S', time.localtime(time.time()))
                with open(self.filepath + '/' + 'MergDat_' + str(times) + '.csv', 'w', encoding='utf-8', newline='') as \
                        file_obj:
                    writer = csv.writer(file_obj)
                    title = ['X','Y','Theta','Radius','dltPos']
                    writer.writerow(title)
                    line = 0
                    for item in self.devpos:
                        contentWr = [ round(self.hdat1[line],6), round(self.hdat2[line],6), round(self.hdat3[line],6), round(self.devpos[line],6), round(self.devthick[line],6) ]
                        writer.writerow(contentWr)
                        line = line + 1

                #self.plot2dats(self.hdat1, self.hdat2,len(self.hdat1),0)        
                #self.plotdats(self.devthick,len(self.devthick),0)
                #self.plotdats(self.hdat3,len(self.devpos),0)
                #self.plotxy(self.hdat1, self.hdat2, 0)

                iMaxTheta = self.hdat3.index(np.max(self.hdat3))
                iMinTheta = self.hdat3.index(np.min(self.hdat3))

                strpathfileMax = self.filepath + '/' + self.FilListStr[iMaxTheta]
                strpathfileMin = self.filepath + '/' + self.FilListStr[iMinTheta]

                numSlot,datsita1,datr_dat1,ret,strtime = self.readStdOfOneFile(strpathfileMax)
                numSlot,datsita2,datr_dat2,ret,strtime = self.readStdOfOneFile(strpathfileMin)

                print(strpathfileMax)
                print(strpathfileMin)

                self.show2Circle(datsita1,datr_dat1,datsita2,datr_dat2)

                self.showMsg()


                self.decodefinish = 1
                #####################################################
            else:
                self.startfle = self.cyccnt * self.fldealnumcyc
                self.endfle = self.startfle + self.fldealnumcyc
                if self.endfle > self.filenum:
                    self.endfle = self.filenum
    
    def showMsg(self):
        strThetaMsg = 'Theta最大值是' + str(np.max(self.hdat3)) + ',\n' + 'Theta最小值是' + str(np.min(self.hdat3)) + ',\n' + 'Theta峰峰值是' + str(np.max(self.hdat3) - np.min(self.hdat3)) + '\n'
        strPosMsg = 'Pos最大值是' + str(np.max(self.devthick)) + ',\n' + 'Pos最小值是' + str(np.min(self.devthick)) + ',\n' + 'Pos峰峰值是' + str(np.max(self.devthick) - np.min(self.devthick)) + '\n'
        self.labelMsg.setText(strThetaMsg + strPosMsg)

    # show curve of the select col
    def showDat(self,index):
        if self.decodefinish == 1 :
            self.plotxy(self.hdat1, self.hdat2, 0)
            if index.column() == 0:
                self.plotdats(self.hdat1,len(self.hdat1),0)
            if index.column() == 1:
                self.plotdats(self.hdat2,len(self.hdat2),0)
            if index.column() == 2:
                self.plotdats(self.hdat3,len(self.hdat3),0)
            if index.column() == 3:
                self.plotdats(self.devpos,len(self.devpos),0)
            if index.column() == 4:
                self.plotdats(self.devthick,len(self.devthick),0)
 
        #print('null operate')

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
        self.cutlowfrq = (1 + self.horizontalSlider.value()) * 20
        self.labelFrq.setText('cutoff frequence change to %dHz' % self.cutlowfrq)

    # ---------------------------------------read the file list of the Directory
    def dirlistfile(self):
        filepath = QFileDialog.getExistingDirectory()
        #filepath = self.tempFilePath
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
            strFilename = file_name[0:8]
            if strFilename == 'MergDat_':
                filemiddle = file_name

        ##########################################################################
        return filemiddle

    # ----------------------------------------analyse the data of the single file and plot the curve
    def analySingleFile(self, filepath):
        numSlot,datsita,datr_dat,ret,strtime = self.readStdOfOneFile(filepath)
    
        # reset Size
        self.resetSize(2 , numSlot)
        # set rowtitles
        self.setRowTitle(0,"sita")
        self.setRowTitle(1,"r_dat")
        # set collum title
        line = 0
        for item in datsita:
            self.setVerTitle(line,str(line))
            line = line + 1
        # set cell value row 0
        line = 0
        for item in datsita:
            # print(objarea[item])
            self.setCellValue(line,0,item)
            line = line + 1

        line = 0
        for item in datr_dat:
            # print(objarea[item])
            self.setCellValue(line,1,item)
            line = line + 1

        self.showCircle(datsita,datr_dat)
        
        self.labelMsg.setText( strtime + '\n X= ' + str(ret[0]) + '\n Y= ' + str(ret[1]) + '\n A= ' + str(ret[2]) + '\n R= ' + str(ret[3]) )

    def showCircle(self,datsita,datr_dat):
        xx=[]
        yy=[]
        for ii in range(0,len(datsita)):
            xx.append(np.cos(datsita[ii] / 100.0 / 180.0 * 3.141592653) * datr_dat[ii] / 1000.0)
            yy.append(np.sin(datsita[ii] / 100.0 / 180.0 * 3.141592653) * datr_dat[ii] / 1000.0)

        self.plotxy(datsita,datr_dat,0)
        self.plotxy(xx,yy,1)

    def show2Circle(self,datsita1,datr_dat1,datsita2,datr_dat2):
        xx=[]
        yy=[]
        xx1=[]
        yy1=[]

        for ii in range(0,len(datsita1)):
            xx.append(np.cos(datsita1[ii] / 100.0 / 180.0 * 3.141592653) * datr_dat1[ii] / 1000.0)
            yy.append(np.sin(datsita1[ii] / 100.0 / 180.0 * 3.141592653) * datr_dat1[ii] / 1000.0)
        for ii in range(0,len(datsita2)):
            xx1.append(np.cos(datsita2[ii] / 100.0 / 180.0 * 3.141592653) * datr_dat2[ii] / 1000.0)
            yy1.append(np.sin(datsita2[ii] / 100.0 / 180.0 * 3.141592653) * datr_dat2[ii] / 1000.0)
        self.plot2xy(xx,yy,xx1,yy1,1)

    # ----------------------------------------function to read std out of one single file
    def readStdOfOneFile(self, filepath):
        with open(filepath) as f:
            rawcontent = f.read()
            content = rawcontent.replace(" ", " ")
            try:
                numSlot = int(content.split('sample:')[1].split('\n')[0])
            except:
                print("no sample")

            content = rawcontent.split('theta	r')[1]
            datsita = []
            datr_dat=[]
            ret=[]
            ret.append(float(rawcontent.split('X=')[1].split(',')[0]) / 1000.0)
            ret.append(float(rawcontent.split('Y=')[1].split(',')[0]) / 1000.0)
            ret.append(float(rawcontent.split('A=')[1].split(',')[0]))
            ret.append(float(rawcontent.split('R=')[1].split('\n')[0])/ 1000.0)
            strtime = (rawcontent.split('time: ')[1].split('\n')[0])

            contentRet = content.split('\n')
            for item in range(1,numSlot+1):
                datsita.append(int(contentRet[item].split('\t')[0]))
                datr_dat.append(int(contentRet[item].split('\t')[1]))

            ########################
            #self.plotxy(datsita,datr_dat,0)
            #print(ret)
            #print(strtime)
            return numSlot,datsita,datr_dat,ret,strtime
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
    mainWindow.move((int)(x), (int)(y))
    mainWindow.show()
    #######################################################
    #figplot = plt.subplots()
    #plt.get_current_fig_manager().window.setGeometry(x + mainWindow.width() + 5, y + 31, 800, 514)
    #plt.show(block=False)
    #######################################################
    sys.exit(app.exec_())
