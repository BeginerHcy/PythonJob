
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow, QSizePolicy, QWidget,QTableWidgetItem,QDesktopWidget
from PyQt5.QtWidgets import QFileDialog
#from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
from fwupdate import Ui_MainWindow
import sys
#import serial
import serial.tools.list_ports
#import time

#import  ctypes

#from ctypes import Structure, c_float, c_uint8, c_uint16

import struct
#from struct import unpack
import os
import serial
import serial.tools.list_ports

from gmssl import func


timeReRead = 50  #means 400ms

class SystemPara_type:

    def __init__(self):
        self.BufferHead = 0
        self.SaveParameter = 0
        self.MeasurePosScale = 0
        self.TargetExchScale = 0
        self.SynVelocity = 0
        self.BendX1 = 0
        self.BendH = 0
        self.BackVel = 0
        self.FollowVelocity = 0
        self.MaualVelocity = 0
        self.ACC = 0
        self.DEC = 0
        self.StartPos = 0
        self.EndPos = 0
        self.BackPosition = 0
        self.OffsetPos = 0
        self.AutoBackPos = 0
        self.OffsetPos2 = 0
        self.offsetBasic = 0
        self.offsetBasic_Teach = 0
        self.PosLimitSw = 0
        self.NegLimitSw = 0
        self.EnableSw = 0
        self.BendAngle = 0
        self.BendPanX = 0
        self.PosLimitSw_B = 0
        self.NegLimitSw_B = 0
        self.ACC_B = 0
        self.DEC_B = 0
        self.MaualVelocity_B = 0
        self.BackPosition_B = 0
        self.BackVel_B = 0
        self.FollowVelocity_B = 0
        self.SynVelocity_B = 0
        self.Distance90Degree = 0
        self.AxisBScale = 0
        self.TeachAngle = 0
        self.EndPos_Teach = 0
        self.PositionOfstBR1 = 0
        self.PositionOfstBR2 = 0
        self.PositionOfstBR3 = 0
        self.PositionOfstBR4 = 0
        self.PositionOfstBR5 = 0
        self.PositionOfstBR6 = 0
        self.PositionOfstBR7 = 0
        self.PositionOfstBR8 = 0
        self.PositionOfstBR9 = 0
        self.PositionOfstBR10 = 0
        self.VmoldeD = 0
        self.VDistMachine = 0
        self.Vmolde2D = 0
        self.SpringH = 0
        self.MoldH = 0
        self.AngleScaleK = 0
        self.EnableSim = 0
        self.MachineZeroOfset = 0
        self.Bend2TimeOfset = 0
        self.AngleB = 0
        self.PlatThick = 0
        self.HoldBendTime = 0
        self.SuckDist = 0

        self.RS485Bauderate = 0
        # 0-9600 1-19200 2-38400 3-115200
        self.RS232Bauderate = 0
        # 0-9600 1-19200 2-38400 3-115200
        self.TTLBauderate = 0
        # 0-9600 1-19200 2-38400 3-115200
        self.CANBusBauderate = 0
        # 0-125k 1-250k 2-500k 3-1000k
        self.AppMode = 0
        self.AOMode = 0
        # 000 : Disable 001:0~5V 002:0~10V 003:+-5V 004:+-10V 005:NULL 006:4~20mA 007:0~20mA 008:0~24mA
        self.cmdSaveParameter = 0
        self.RS485Node = 0
        self.CanNode = 0
        self.RangeMode = []*4
        ##BoardType 0 :Null  1: A-Type
        self.BoardType = 0
        self.MachineZeroOfsetTemp = 0
        self.Pitch = 0
        self.Peri_meter = 0
        self.Ratios = 0
        self.RevPulse = 0
        self.PayloadType = 0
        self.MachineType = 0
        self.decLevel = 0
        self.FirmwareVersion = 0

       # self.MachineCode = str("")



class DownloadCtrl:

    def __init__(self):
        self.step = 0
        self.rebooted = 0
        self.started = 0
        self.error = 0
        self.ended = 0
        self.fwlen = 0
        self.index = 0
        self.opened=0
        self.dwnIndex=0
        self.dwnOK=0
        self.status=0


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # 设置应用程序的窗口图标
        self.setWindowIcon(QIcon("./Resourse/icon.png"))
        #######################################################
        # 串口无效
        self.ser = None
        self.refresh()
        # 实例化一个定时器
        self.timer = QTimer(self)

        self.timer_Main = QTimer(self)

        # 定时器调用读取串口接收数据
        self.timer.timeout.connect(self.recv)

        self.timer_Main.timeout.connect(self.CycMain)
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
        # 打开bin文件
        self.selBinfile.triggered.connect(self.selBin)
        # 读取参数
        self.readSysPara.triggered.connect(self.readMachinePara)
        # 下载参数
        self.writeSysPara.triggered.connect(self.downMachinePara)
        #显示工具版本
        self.version.triggered.connect(self.showVersion)
        #更新固件
        self.updateFirmware.triggered.connect(self.writeCommand)

        # 执行一下打开串口
        self.revdata=bytearray(300)
        self.fill=300
        self.decode=300
        self.receive_num=False
        self.lenRevdata = False
        self.timeStamp = 0
        ##############################
        self.wrteProcess = 0
        ##############################
        self.disconnect.setEnabled(False)
        self.updateFirmware.setEnabled(False)
        self.readSysPara.setEnabled(False)
        self.writeSysPara.setEnabled(False)
        self.BarWriteProcess.setValue(self.wrteProcess)
        ##############################
        self.DwnCtrl = DownloadCtrl()
        self.gSystemPara = SystemPara_type()
        self.cmdWrite = False
        self.binfile = 0
        self.filepath = 'fw.bin'
        self.oldtimeStamp = 0
        self.tempSend = 0
        self.fileSelected = 0
        self.comopened = 0
        self.cmbBrdrate.setCurrentIndex(3)
        self.BinFileLable.setText('(.bin)')
        self.version = str('Version: V21.0830.01')
        self.readPar=0
        self.writePar=0

        self.timer1 = timeReRead
        self.timer2 = timeReRead

    def showVersion(self):
        QMessageBox.information(self, 'MachineUpdate', self.version)

    def selBin(self):
        try:
            filepath =  QFileDialog.getOpenFileName(self,'选择固件','','bin files(*.bin , *.BIN)')
            self.filepath = filepath[0]
            if(len(self.filepath)>3):
                self.fileSelected = 1
                if (self.comopened == 1):
                    self.updateFirmware.setEnabled(True)
                for istr in range(len(self.filepath), 1, -1):
                    if self.filepath[istr-1] == '/':
                        self.BinFileLable.setText(self.filepath[istr:len(self.filepath)])
                        break;

        except:
            self.statusbar.showMessage('File not selected !')



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

    def resetDwn(self):
        self.cmdWrite = False
        self.DwnCtrl.rebooted = 0
        self.DwnCtrl.step = 0
        self.DwnCtrl.started = 0
        self.DwnCtrl.error = 0
        self.DwnCtrl.ended = 0
        self.DwnCtrl.fwlen = 0
        self.DwnCtrl.index = 0
        self.DwnCtrl.opened = 0
        self.DwnCtrl.dwnIndex = 0
        self.DwnCtrl.dwnOK = 0
        self.DwnCtrl.status = 0

    # 重载窗口关闭事件
    def closeEvent(self, e):
        # 关闭定时器，停止读取接收数据
        self.timer.stop()
        self.timer_Main.stop()
        # 关闭串口
        if self.ser != None:
            self.ser.close()

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
            self.ser = serial.Serial(self.cmbComlist.currentText(), int(self.cmbBrdrate.currentText()), timeout=0.2)
            self.comopened = 1
        except:
            QMessageBox.critical(self, 'com', '没有可用的串口或当前串口被占用')
            return None
        # 字符间隔超时时间设置
        self.ser.interCharTimeout = 0.0001
        # 1ms的单位
        self.timer.start(10)
        self.timer_Main.start(10)
        self.statusbar.showMessage('communication opened.')
        ###############Button status###############
        self.connect.setEnabled(False)
        self.disconnect.setEnabled(True)
        self.readSysPara.setEnabled(True)

        if (self.fileSelected == 1):
            self.updateFirmware.setEnabled(True)




    # 关闭串口
    def comclose(self):
        self.timer.stop()
        self.cmdWrite=False
        self.timer_Main.stop()
        self.resetDwn()
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
        self.updateFirmware.setEnabled(False)
        self.readSysPara.setEnabled(False)
        self.writeSysPara.setEnabled(False)
        self.btnMachine.setEnabled(False)
        self.SysParatable.setEnabled(False)
        self.readPar = 0
        self.writePar = 0



    def sendBin(self):

        len = 240

        if self.DwnCtrl.ended==1:
            self.binfile.close()
            self.DwnCtrl.opened = 0
            self.DwnCtrl.status = 200
            if (self.fileSelected == 1):
                self.updateFirmware.setEnabled(True)
            print('close')
            print(self.timeStamp)
            self.statusbar.showMessage('Finish!')
            #self.cmdWrite = False
            QMessageBox.information(self,'恭喜', '固件更新完成！')
            return None
        ###########################################
        if self.DwnCtrl.index + len > self.DwnCtrl.fwlen:
            numRead = self.DwnCtrl.fwlen % len
        else:
            numRead = len
        #print(numRead)
        self.DwnCtrl.dwnOK = 0
        ###########################################
        data = self.binfile.read(numRead)
        ###########################################
        indexHL = [0, 0, 0, 0, 0, 0, 0]

        indexHL[0] = self.DwnCtrl.index >> 16 & 255
        indexHL[1] = self.DwnCtrl.index >> 8 & 255
        indexHL[2] = self.DwnCtrl.index >> 0 & 255

        indexHL[3] = self.DwnCtrl.fwlen >> 16 & 255
        indexHL[4] = self.DwnCtrl.fwlen >> 8 & 255
        indexHL[5] = self.DwnCtrl.fwlen >> 0 & 255

        indexHL[6] = numRead
        ###########################################
        sendbuf = [0xAA]
        sendbuf.extend(indexHL)
        sendbuf.extend(func.bytes_to_list(data))
        ###########################################
        crc = crc16(sendbuf)
        crcHL = [0, 0]
        crcHL[1] = crc >> 8
        crcHL[0] = crc >> 0 & 255
        ###########################################
        sendbuf.extend(crcHL)
        self.tempSend = sendbuf
        self.ser.write(sendbuf)
        self.DwnCtrl.status = 24
        #print(sendbuf)
        ###########################################
        self.DwnCtrl.index = self.DwnCtrl.index + numRead
        if self.DwnCtrl.index >= self.DwnCtrl.fwlen:
            self.DwnCtrl.ended = 1
        ###########################################

    def sendStartDwn(self):
        sendbuf = [0xAB,1]
        ###########################################
        crc = crc16(sendbuf)
        crcHL = [0, 0]
        crcHL[1] = crc >> 8
        crcHL[0] = crc >> 0 & 255
        ###########################################
        sendbuf.extend(crcHL)
        self.ser.write(sendbuf)
        self.DwnCtrl.status = 2
        print(sendbuf)
    def readMachinePara(self):
        sendbuf = [0xAB,0xFF]
        ###########################################
        crc = crc16(sendbuf)
        crcHL = [0, 0]
        crcHL[1] = crc >> 8
        crcHL[0] = crc >> 0 & 255
        ###########################################
        sendbuf.extend(crcHL)
        self.ser.write(sendbuf)
        self.DwnCtrl.status = 2
        self.readPar = 1
        self.readSysPara.setEnabled(False)
        self.writeSysPara.setEnabled(False)

    def sendEndDwn(self):
        sendbuf = [0xAC,1]
        ###########################################
        crc = crc16(sendbuf)
        crcHL = [0, 0]
        crcHL[1] = crc >> 8
        crcHL[0] = crc >> 0 & 255
        ###########################################
        sendbuf.extend(crcHL)
        self.ser.write(sendbuf)
        self.DwnCtrl.status = 210

    # 串口发送数据处理
    def CycMain(self):
        self.timeStamp = self.timeStamp + 0.01
        #self.CapRebootOK()
        #print(self.DwnCtrl.status)
        #self.statusbar.showMessage(str(self.DwnCtrl.index))
        if self.cmdWrite == True:
            if(self.DwnCtrl.status==0):
                self.sendStartDwn()
                self.oldtimeStamp = self.timeStamp
                self.statusbar.showMessage('Reboot command')
            elif(self.DwnCtrl.status==2):
                self.CapAskDwn()
                if (self.timeStamp - self.oldtimeStamp)>2.0:
                    self.DwnCtrl.status = 0
            elif(self.DwnCtrl.status==10):
                self.CapRebootOK()
                self.statusbar.showMessage('Reboot ok')
            elif(self.DwnCtrl.status==20):
                self.sendBin()
                self.oldtimeStamp = self.timeStamp

            elif(self.DwnCtrl.status==24):
                self.CapDwnBinOK()
                self.statusbar.showMessage('Downloading!')
                if(self.DwnCtrl.dwnOK==1):
                    self.DwnCtrl.status = 20
                if(self.timeStamp - self.oldtimeStamp > 2.0):
                    self.ser.write(self.tempSend)
                    self.oldtimeStamp = self.timeStamp
                    print('send lose')

            elif(self.DwnCtrl.status==200):
                self.sendEndDwn()
            elif(self.DwnCtrl.status==210):
                self.CapFinish()
            elif(self.DwnCtrl.status==255):
                self.cmdWrite = False
                self.resetDwn()
        else:

            if(self.readPar == 1):
                self.CapMachinePar()
                if(self.timer1<1):
                    self.readMachinePara()
                    self.timer1 = timeReRead
                else:
                    self.timer1 = self.timer1 - 1
            else:
                self.timer1 = timeReRead

            if(self.writePar == 1):
                self.CapwritePar()
                if(self.timer2<1):
                    self.downMachinePara()
                    self.timer2 = timeReRead
                else:
                    self.timer2 = self.timer2 - 1
            else:
                self.timer2 = timeReRead


    def writeCommand(self):
        if self.cmdWrite == False:
            if self.DwnCtrl.opened==0:
                try:
                    self.binfile = open(file=self.filepath,mode='rb')
                    self.resetDwn()
                    self.BarWriteProcess.setValue(0)
                    self.DwnCtrl.fwlen = os.path.getsize(self.filepath)
                    print(self.DwnCtrl.fwlen)
                    print('opened')
                    self.cmdWrite = True
                    self.DwnCtrl.opened = 1
                    print(self.timeStamp)
                    self.updateFirmware.setEnabled(False)
                except:
                    QMessageBox.critical(self,'固件更新','请重新选择固件！')
                    self.resetDwn()
            else:
                self.cmdWrite = True

    def downMachinePara(self):

        self.gSystemPara.Pitch = float(self.SysParatable.item(53,0).text())
        self.gSystemPara.Peri_meter = float(self.SysParatable.item(54, 0).text())
        self.gSystemPara.Ratios = float(self.SysParatable.item(55, 0).text())
        self.gSystemPara.RevPulse = float(self.SysParatable.item(56, 0).text())
        self.gSystemPara.MachineType = int(self.SysParatable.item(57, 0).text())
        self.gSystemPara.decLevel = int(self.SysParatable.item(58, 0).text())
        self.gSystemPara.PayloadType = self.cmbETYPE.currentIndex()

        Pitch = round(self.gSystemPara.Pitch * 100)
        Peri_meter = round(self.gSystemPara.Peri_meter * 100)
        Ratios = round(self.gSystemPara.Ratios * 100)
        RevPulse = round(self.gSystemPara.RevPulse)
        PayloadType = self.gSystemPara.PayloadType
        MachineType = self.gSystemPara.MachineType
        decLevel = self.gSystemPara.decLevel

        #print(self.SysParatable.item(58,0).text())
        #print(RevPulse)
        #print(Ratios)

        sendbuf = [0]*41
        sendbuf[0] = 0xAD
        sendbuf[1] = Pitch >> 8
        sendbuf[2] = Pitch >> 0 & 255

        sendbuf[3] = Peri_meter >> 8
        sendbuf[4] = Peri_meter >> 0 & 255

        sendbuf[5] = Ratios >> 8
        sendbuf[6] = Ratios >> 0 & 255

        sendbuf[7] = RevPulse >> 8
        sendbuf[8] = RevPulse >> 0 & 255

        sendbuf[9] = PayloadType
        sendbuf[10] = MachineType
        sendbuf[11] = decLevel

        ###########################################
        crc = crc16(sendbuf)
        crcHL = [0, 0]
        crcHL[1] = crc >> 8
        crcHL[0] = crc >> 0 & 255
        ###########################################
        sendbuf.extend(crcHL)
        self.ser.write(sendbuf)
        self.writePar = 1
        #print(sendbuf)
        ###########################################
        self.writeSysPara.setEnabled(False)
        self.readSysPara.setEnabled(False)
        ###########################################

    def CapDwnBinOK(self):
        len=7
        icrc=len-2
        ######################################################################################
        if self.lenRevdata>=len:#DwnBinOK is 6 bytes
            for i in range(self.decode,self.fill-1):
                if self.fill >= i+len:
                    if (self.revdata[i] == 0xBA):
                        crc=crc16(self.revdata[i:i+len-2])
                        if(self.revdata[i+icrc] + self.revdata[i+icrc+1]*256)==crc:

                            if self.revdata[i+1]==1:
                                self.DwnCtrl.dwnIndex = self.revdata[i+2]*65536 + self.revdata[i+3]*256 + self.revdata[i+4]
                                if self.DwnCtrl.dwnIndex == self.DwnCtrl.index:
                                    self.DwnCtrl.dwnOK = 1
                                    #print('dwnOK')
                                    self.BarWriteProcess.setValue(100 * self.DwnCtrl.dwnIndex/self.DwnCtrl.fwlen)
                                    ###########################################
                                    self.decode = i + len - 1#refresh the decode index
                                    self.lenRevdata = self.fill - self.decode#update buf
                                    ###########################################
                                else:
                                    self.DwnCtrl.dwnOK = 0
                            else:
                                self.DwnCtrl.dwnOK = 0

    def CapwritePar(self):
        len=4
        icrc=len-2
        ######################################################################################
        if self.lenRevdata>=len:#CapwritePar is 6 bytes
            for i in range(self.decode,self.fill-1):
                if self.fill >= i+len:
                    testa = self.revdata[i]
                    if (self.revdata[i] == 0xBD):
                        crc=crc16(self.revdata[i:i+len-2])
                        if(self.revdata[i+icrc] + self.revdata[i+icrc+1]*256)==crc:
                            if self.revdata[i+1]==1:
                                self.writePar = 0
                            ###########################################
                            self.writeSysPara.setEnabled(True)
                            self.readSysPara.setEnabled(True)
                            QMessageBox.information(self,"下载参数","成功！！")
                            ###########################################
                            self.decode = i + len - 1  # refresh the decode index
                            self.lenRevdata = self.fill - self.decode  # update buf
                            ###########################################

    def CapRebootOK(self):
        len=4
        icrc=len-2
        ######################################################################################
        if self.lenRevdata>=len:#DwnBinOK is 6 bytes
            for i in range(self.decode,self.fill-1):
                if self.fill >= i+len:
                    testa = self.revdata[i]
                    if (self.revdata[i] == 0xDB):
                        crc=crc16(self.revdata[i:i+len-2])
                        if(self.revdata[i+icrc] + self.revdata[i+icrc+1]*256)==crc:
                            if self.revdata[i+1]==1:
                                if (self.DwnCtrl.status == 10):
                                    self.DwnCtrl.status = 20
                                    self.DwnCtrl.rebooted = 1
                                print('controller reboot')
                            else:
                                self.DwnCtrl.rebooted = 0
                            ###########################################
                            self.decode = i + len - 1  # refresh the decode index
                            self.lenRevdata = self.fill - self.decode  # update buf
                            #print(self.decode)
                            ###########################################
    def CapMachinePar(self):
        len=298
        icrc=len-2
        ######################################################################################
        if self.lenRevdata>=len:#DwnBinOK is 6 bytes
            for i in range(self.decode,self.fill-1):
                if self.fill >= i+len:
                    if (self.revdata[i] == 0xAB):
                        crc=crc16(self.revdata[i:i+len-2])
                        if(self.revdata[i+icrc] + self.revdata[i+icrc+1]*256)==crc:
                            #print(self.revdata)
                            self.gSystemPara.BufferHead                     = struct.unpack("c",  self.revdata[i      :i + 1])[0]
                            self.gSystemPara.SaveParameter                  = struct.unpack("c",  self.revdata[i + 1  :i + 2])[0]
                            self.gSystemPara.MeasurePosScale                = struct.unpack("<f", self.revdata[i + 4  :i + 8])[0]
                            self.gSystemPara.TargetExchScale                = struct.unpack("<f", self.revdata[i + 8  :i + 12])[0]
                            self.gSystemPara.SynVelocity                    = struct.unpack("<f", self.revdata[i + 12 :i + 16])[0]

                            self.gSystemPara.BendX1                         = struct.unpack("<f", self.revdata[i + 16:i + 20])[0]
                            self.gSystemPara.BendH                          = struct.unpack("<f", self.revdata[i + 20:i + 24])[0]
                            self.gSystemPara.BackVel                        = struct.unpack("<f", self.revdata[i + 24:i + 28])[0]
                            self.gSystemPara.FollowVelocity                 = struct.unpack("<f", self.revdata[i + 28:i + 32])[0]
                            self.gSystemPara.MaualVelocity                  = struct.unpack("<f", self.revdata[i + 32:i + 36])[0]
                            self.gSystemPara.ACC                            = struct.unpack("<f", self.revdata[i + 36:i + 40])[0]
                            self.gSystemPara.DEC                            = struct.unpack("<f", self.revdata[i + 40:i + 44])[0]
                            self.gSystemPara.StartPos                       = struct.unpack("<f", self.revdata[i + 44:i + 48])[0]
                            self.gSystemPara.EndPos                         = struct.unpack("<f", self.revdata[i + 48:i + 52])[0]
                            self.gSystemPara.BackPosition                   = struct.unpack("<f", self.revdata[i + 52:i + 56])[0]
                            self.gSystemPara.OffsetPos                      = struct.unpack("<f", self.revdata[i + 56:i + 60])[0]
                            self.gSystemPara.AutoBackPos                    = struct.unpack("<f", self.revdata[i + 60:i + 64])[0]
                            self.gSystemPara.OffsetPos2                     = struct.unpack("<f", self.revdata[i + 64:i + 68])[0]
                            self.gSystemPara.offsetBasic                    = struct.unpack("<f", self.revdata[i + 68:i + 72])[0]
                            self.gSystemPara.offsetBasic_Teach              = struct.unpack("<f", self.revdata[i + 72:i + 76])[0]
                            self.gSystemPara.PosLimitSw                     = struct.unpack("<f", self.revdata[i + 76:i + 80])[0]
                            self.gSystemPara.NegLimitSw                     = struct.unpack("<f", self.revdata[i + 80:i + 84])[0]
                            self.gSystemPara.EnableSw                       = struct.unpack("?",  self.revdata[i + 84:i + 85])[0]

                            self.gSystemPara.BendAngle                      = struct.unpack("<f", self.revdata[i + 88:i + 92])[0]
                            self.gSystemPara.BendPanX                       = struct.unpack("<f", self.revdata[i + 92:i + 96])[0]
                            self.gSystemPara.PosLimitSw_B                               = struct.unpack("<f", self.revdata[i + 96:i + 100])[0]
                            self.gSystemPara.NegLimitSw_B                               = struct.unpack("<f", self.revdata[i + 100:i + 104])[0]
                            self.gSystemPara.ACC_B                                      = struct.unpack("<f", self.revdata[i + 104:i + 108])[0]
                            self.gSystemPara.DEC_B                                      = struct.unpack("<f", self.revdata[i + 108:i + 112])[0]
                            self.gSystemPara.MaualVelocity_B                            = struct.unpack("<f", self.revdata[i + 112:i + 116])[0]
                            self.gSystemPara.BackPosition_B                             = struct.unpack("<f", self.revdata[i + 116:i + 120])[0]
                            self.gSystemPara.BackVel_B                                  = struct.unpack("<f", self.revdata[i + 120:i + 124])[0]
                            self.gSystemPara.FollowVelocity_B                           = struct.unpack("<f", self.revdata[i + 124:i + 128])[0]
                            self.gSystemPara.SynVelocity_B                              = struct.unpack("<f", self.revdata[i + 128:i + 132])[0]
                            self.gSystemPara.Distance90Degree                           = struct.unpack("<f", self.revdata[i + 132:i + 136])[0]
                            self.gSystemPara.AxisBScale                                 = struct.unpack("<f", self.revdata[i + 136:i + 140])[0]
                            self.gSystemPara.TeachAngle                                 = struct.unpack("<f", self.revdata[i + 140:i + 144])[0]
                            self.gSystemPara.EndPos_Teach                               = struct.unpack("<f", self.revdata[i + 144:i + 148])[0]

                            self.gSystemPara.PositionOfstBR1                          = struct.unpack("<f", self.revdata[i + 148:i + 152])[0]
                            self.gSystemPara.PositionOfstBR2 = struct.unpack("<f", self.revdata[i + 152:i + 156])[0]
                            self.gSystemPara.PositionOfstBR3 = struct.unpack("<f", self.revdata[i + 156:i + 160])[0]
                            self.gSystemPara.PositionOfstBR4 = struct.unpack("<f", self.revdata[i + 160:i + 164])[0]
                            self.gSystemPara.PositionOfstBR5 = struct.unpack("<f", self.revdata[i + 164:i + 168])[0]
                            self.gSystemPara.PositionOfstBR6 = struct.unpack("<f", self.revdata[i + 168:i + 172])[0]
                            self.gSystemPara.PositionOfstBR7 = struct.unpack("<f", self.revdata[i + 172:i + 176])[0]
                            self.gSystemPara.PositionOfstBR8 = struct.unpack("<f", self.revdata[i + 176:i + 180])[0]
                            self.gSystemPara.PositionOfstBR9 = struct.unpack("<f", self.revdata[i + 180:i + 184])[0]
                            self.gSystemPara.PositionOfstBR10 = struct.unpack("<f", self.revdata[i + 184:i + 188])[0]

                            self.gSystemPara.VmoldeD                                    = struct.unpack("<f", self.revdata[i + 188:i + 192])[0]
                            self.gSystemPara.VDistMachine                               = struct.unpack("<f", self.revdata[i + 192:i + 196])[0]
                            self.gSystemPara.Vmolde2D                                   = struct.unpack("<f", self.revdata[i + 196:i + 200])[0]
                            self.gSystemPara.SpringH                                    = struct.unpack("<f", self.revdata[i + 200:i + 204])[0]
                            self.gSystemPara.MoldH                                      = struct.unpack("<f", self.revdata[i + 204:i + 208])[0]
                            self.gSystemPara.AngleScaleK                                = struct.unpack("<f", self.revdata[i + 208:i + 212])[0]

                            self.gSystemPara.EnableSim                      = struct.unpack("?", self.revdata[i + 212:i + 213])[0]

                            self.gSystemPara.MachineZeroOfset               = struct.unpack("<f", self.revdata[i + 216:i + 220])[0]
                            self.gSystemPara.Bend2TimeOfset                 = struct.unpack("<f", self.revdata[i + 220:i + 224])[0]
                            self.gSystemPara.AngleB                         = struct.unpack("<f", self.revdata[i + 224:i + 228])[0]
                            self.gSystemPara.PlatThick                      = struct.unpack("<f", self.revdata[i + 228:i + 232])[0]
                            self.gSystemPara.HoldBendTime                   = struct.unpack("<f", self.revdata[i + 232:i + 236])[0]
                            self.gSystemPara.SuckDist                       = struct.unpack("<f", self.revdata[i + 236:i + 240])[0]

                            self.gSystemPara.RS485Bauderate                 = struct.unpack("c", self.revdata[i + 240:i + 241])[0]
                            self.gSystemPara.RS232Bauderate                 = struct.unpack("c", self.revdata[i + 241:i + 242])[0]
                            self.gSystemPara.TTLBauderate                   = struct.unpack("c", self.revdata[i + 242:i + 243])[0]
                            self.gSystemPara.CANBusBauderate                = struct.unpack("c", self.revdata[i + 243:i + 244])[0]

                            self.gSystemPara.AppMode                        = struct.unpack("c", self.revdata[i + 244:i + 245])[0]
                            self.gSystemPara.AOMode                         = struct.unpack("c", self.revdata[i + 245:i + 246])[0]
                            self.gSystemPara.cmdSaveParameter               = struct.unpack("c", self.revdata[i + 246:i + 247])[0]
                            self.gSystemPara.RS485Node                      = struct.unpack("c", self.revdata[i + 247:i + 248])[0]

                            self.gSystemPara.CanNode                        = struct.unpack("c", self.revdata[i + 248:i + 249])[0]
                            #self.gSystemPara.RangeMode[0]
                            # self.gSystemPara.RangeMode[1]
                            # self.gSystemPara.RangeMode[2]

                            # self.gSystemPara.RangeMode[3]
                            # self.gSystemPara.BoardType
                            #
                            #

                            self.gSystemPara.MachineZeroOfsetTemp           = struct.unpack("<f", self.revdata[i + 256:i + 260])[0]

                            self.gSystemPara.Pitch                          = struct.unpack("<f", self.revdata[i + 260:i + 264])[0]
                            self.gSystemPara.Peri_meter                     = struct.unpack("<f", self.revdata[i + 264:i + 268])[0]
                            self.gSystemPara.Ratios                         = struct.unpack("<f", self.revdata[i + 268:i + 272])[0]
                            self.gSystemPara.RevPulse                       = struct.unpack("<f", self.revdata[i + 272:i + 276])[0]

                            self.gSystemPara.PayloadType                    = (struct.unpack("B", self.revdata[i + 276:i + 277])[0])
                            self.gSystemPara.MachineType                    = (struct.unpack("B", self.revdata[i + 277:i + 278])[0])
                            self.gSystemPara.decLevel                       = (struct.unpack("B", self.revdata[i + 278:i + 279])[0])
                            #                                               = (struct.unpack("B", self.revdata[i + 279:i + 280])[0])
                            self.gSystemPara.FirmwareVersion                = (struct.unpack("L", self.revdata[i + 280:i + 284])[0])

                            #print(self.gSystemPara.FirmwareVersion)

                            #for j in range(i + 278 , i + 276 + 19):
                            #    if self.revdata[j]== 0x00:
                            #        endj = j
                            #        break;

                            #self.gSystemPara.MachineCode =  (self.revdata[i + 278:endj]).decode('utf-8')

                            self.writeSysPara.setEnabled(True)
                            self.btnMachine.setEnabled(True)
                            self.SysParatable.setEnabled(True)
                            self.resize(400, 800)
                            screen = QDesktopWidget().screenGeometry()
                            # 获取窗口坐标系
                            size = self.geometry()

                            newLeft = (screen.width() - size.width()) / 2
                            newTop = (screen.height() - size.height()) / 2

                            if (self.geometry().y()+800 > screen.height()):
                                self.move(size.x() - 8, int(newTop))

                            QMessageBox.information(self, '参数读取', '成功！！')
                            self.displaySystmPara()
                            self.readSysPara.setEnabled(True)

                            #self.SysParatable.setItem(1, 0, QTableWidgetItem(str(1.234)))

                            self.readPar = 0
                            ###########################################
                            self.decode = i + len - 1  # refresh the decode index
                            self.lenRevdata = self.fill - self.decode  # update buf
                            #print(self.decode)
                            ###########################################
    def CapAskDwn(self):
        len=4
        icrc=len-2
        ######################################################################################
        if self.lenRevdata>=len:#DwnBinOK is 6 bytes
            for i in range(self.decode,self.fill-1):
                if self.fill >= i+len:
                    if (self.revdata[i] == 0xBB):
                        crc=crc16(self.revdata[i:i+len-2])
                        if(self.revdata[i+icrc] + self.revdata[i+icrc+1]*256)==crc:
                            if self.revdata[i+1]==1:
                                self.DwnCtrl.status = 10
                                print('askDwn')
                            ###########################################
                            self.decode = i + len - 1  # refresh the decode index
                            self.lenRevdata = self.fill - self.decode  # update buf
                            #print(self.decode)
                            ###########################################


    def setTabHorValue(self,index,HorValue):
        self.SysParatable.setItem(index, 0, QTableWidgetItem(str(HorValue)))
        #item = QTableWidgetItem(index)
        #item.setFlags( QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled )
        #self.SysParatable.setItem(index, 0, item)
        return index + 1

    def displaySystmPara(self):

        iHorVal = 0
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.MeasurePosScale)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.TargetExchScale)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.SynVelocity)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.BendX1)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.BendH)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.BackVel)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.FollowVelocity)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.MaualVelocity)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.ACC)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.DEC)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.StartPos)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.EndPos)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.BackPosition)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.OffsetPos)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.AutoBackPos)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.OffsetPos2)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.offsetBasic)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.offsetBasic_Teach)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.PosLimitSw)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.NegLimitSw)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.EnableSw)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.BendAngle)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.BendPanX)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.PosLimitSw_B)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.NegLimitSw_B)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.ACC_B)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.DEC_B)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.MaualVelocity_B)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.BackPosition_B)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.BackVel_B)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.FollowVelocity_B)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.SynVelocity_B)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.Distance90Degree)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.AxisBScale)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.TeachAngle)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.EndPos_Teach)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.PositionOfstBR1)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.PositionOfstBR2)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.PositionOfstBR3)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.VmoldeD)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.VDistMachine)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.Vmolde2D)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.SpringH)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.MoldH)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.AngleScaleK)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.EnableSim)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.MachineZeroOfset)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.Bend2TimeOfset)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.AngleB)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.PlatThick)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.HoldBendTime)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.SuckDist)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.MachineZeroOfsetTemp)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.Pitch)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.Peri_meter)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.Ratios)
        iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.RevPulse)
        iHorVal = self.setTabHorValue(iHorVal, self.gSystemPara.MachineType)
        iHorVal = self.setTabHorValue(iHorVal, self.gSystemPara.decLevel)
        iHorVal = self.setTabHorValue(iHorVal, self.gSystemPara.PayloadType)
        iHorVal = self.setTabHorValue(iHorVal, self.gSystemPara.FirmwareVersion)



        self.cmbETYPE.setCurrentIndex(self.gSystemPara.PayloadType)

        #iHorVal = self.setTabHorValue(iHorVal,self.gSystemPara.MachineCode)
        #iHorVal = self.setTabHorValue(self, index=iHorVal, HorValue=self.gSystemPara.EndPos_Teach)



    def CapFinish(self):
        len=4
        icrc=len-2
        ######################################################################################
        if self.lenRevdata>=len:#DwnBinOK is 6 bytes
            for i in range(self.decode,self.fill-1):
                if self.fill >= i+len:
                    if (self.revdata[i] == 0xBC):
                        crc=crc16(self.revdata[i:i+len-2])
                        if(self.revdata[i+icrc] + self.revdata[i+icrc+1]*256)==crc:
                            if self.revdata[i+1]==1:
                                self.DwnCtrl.status = 255
                        ###########################################
                        self.decode = i + len - 1  # refresh the decode index
                        self.lenRevdata = self.fill - self.decode  # update buf
                        #print(self.decode)
                        ###########################################


    def recv(self):
        try:
            num = self.ser.inWaiting()
        except:
            self.timer.stop()
            # 串口拔出错误，关闭定时器
            self.ser.close()
            self.ser = None
            # 设置为打开按钮状态
            print('serial error!')
            return None
        if (num > 0):
            # 有时间会出现少读到一个字符的情况，还得进行读取第二次，所以多读一个
            revdata = self.ser.read(num)
            num = len(revdata)
            self.fill = num + self.fill
            self.revdata.extend(revdata)
            if self.fill>300:
                begin_i = self.fill - 300
                self.decode = self.decode - begin_i
                self.revdata = self.revdata[begin_i:self.fill]
                self.fill = 300
            if self.decode<0:
                self.decode = 0
            self.lenRevdata = self.fill - self.decode
            #print(self.revdata)


def crc16(x):
    a = 0xFFFF
    b = 0xA001
    for byte in x:
        #a ^= ord(byte)
        a ^= byte
        for i in range(8):
            last = a % 2
            a >>= 1
            if last == 1:
                a ^= b
    return a
   # s = hex(a).upper()
   # print(a)
   # return s[4:6] + s[2:4] if invert == True else s[2:4] + s[4:6]

if __name__=='__main__':

    app = QtWidgets.QApplication(sys.argv)
   # splash = QtWidgets.QSplashScreen(QtGui.QPixmap("Resourse/splash.png"))
   # splash.show()
    #time.sleep(1.0)
    mainWindow = MainWindow()
    mainWindow.show()
#    splash.finish(mainWindow)
    sys.exit(app.exec_())