# -*- coding: utf-8 -*-

# FileName : main.py
# Version  : V1.0
# Author   : zhou
# DateTime : 2019/7/26
# SoftWare : PyCharm

import sys
from mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore
from threading import Timer
from datetime import datetime
import serial
import configparser
import time
import codecs

TOOLS_FILE_NAME = "tools.ini"
TOOLS_SECT_NAME = "uart"
LOG_FILE_PATH = "./log/"

class RecvThread(QtCore.QThread):
    """
    serial receive thread.
    """
    def __init__(self, ser, showRecvMsg):
        super(RecvThread, self).__init__()
        self.ser = ser
        self.show = showRecvMsg
        # print("create thread")

    def run(self):
        # print("start thread")
        while True:
            count = self.ser.inWaiting()
            if count != 0:
                msg = self.ser.read(count)          # read serial message
                # msg = b'01 02 03 04 05' or b'\x01\x02\x80\x00\xAA\xFF'
                self.show(msg)                      # show receive message
                # self.ser.flushInput()               # clear receive buffer

            time.sleep(0.005)

            if self.ser.isOpen() == False:
                print("close thread")
                self.quit()
                return

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    m_param = {}
    m_count = [0, 0]
    m_serial = serial.Serial()

    m_callback = 0
    m_recvsize = 0
    m_recvetx = 0

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        """
        initial UI.
        """
        self.cmbPort.addItem("COM1")
        self.cmbPort.addItem("COM2")
        self.cmbPort.addItem("COM3")
        self.cmbPort.addItem("COM4")
        self.cmbPort.addItem("COM5")
        self.cmbPort.addItem("COM6")
        self.cmbPort.addItem("COM7")
        self.cmbPort.addItem("COM8")

        self.cmbBaudrate.addItem("1200")
        self.cmbBaudrate.addItem("2400")
        self.cmbBaudrate.addItem("4800")
        self.cmbBaudrate.addItem("9600")
        self.cmbBaudrate.addItem("19200")
        self.cmbBaudrate.addItem("38400")
        self.cmbBaudrate.addItem("57600")
        self.cmbBaudrate.addItem("115200")

        self.cmbByteSize.addItem("5")
        self.cmbByteSize.addItem("6")
        self.cmbByteSize.addItem("7")
        self.cmbByteSize.addItem("8")

        self.cmbStopBits.addItem("1")
        self.cmbStopBits.addItem("1.5")
        self.cmbStopBits.addItem("2")

        self.cmbParity.addItem("None")
        self.cmbParity.addItem("Odd")
        self.cmbParity.addItem("Even")

        # add count label to statusbar
        self.statusbar.addPermanentWidget(self.lblRecvCnt)
        self.statusbar.addPermanentWidget(self.lblSendCnt)

        self.btnOpenPort.clicked.connect(self.on_openPort_clicked)
        self.btnClearWin.clicked.connect(self.on_clearWin_clicked)
        self.btnSaveWin.clicked.connect(self.on_saveWin_clicked)
        self.btnManualSend.clicked.connect(self.on_manualSend_clicked)
        self.btnClose.clicked.connect(self.on_close_clicked)
        self.chkTimeSend.clicked.connect(self.on_timeSend_clicked)

        self.chkHexSend.setChecked(True)
        self.chkHexShow.setChecked(True)
        self.chkTimeSend.setChecked(False)
        self.linTimeNum.setText("1000")

        self.readParamFromFile(TOOLS_FILE_NAME, TOOLS_SECT_NAME)
        self.paramToUI()
        self.updateUI()
        self.showCount(self.m_count)

    def updateUI(self):
        """
        update UI.
        """
        if self.m_serial.is_open == True:
            self.btnOpenPort.setText("关闭串口")
            self.grpOpen.setEnabled(False)
            self.chkTimeSend.setEnabled(True)
            self.btnManualSend.setEnabled(True)

            s = self.cmbPort.currentText() + " is opened, "
            s += self.cmbBaudrate.currentText() + " "
            s += self.cmbByteSize.currentText() + " "
            s += self.cmbStopBits.currentText() + " "
            s += self.cmbParity.currentText() + " "
            self.statusbar.showMessage(s)
        else:
            self.btnOpenPort.setText("打开串口")
            self.grpOpen.setEnabled(True)
            self.chkTimeSend.setEnabled(False)
            self.chkTimeSend.setChecked(False)
            self.btnManualSend.setEnabled(False)

            self.statusbar.showMessage("")

    def paramToUI(self):
        """
        parameter to UI.
        """
        self.cmbPort.setCurrentText(self.m_param['port'])
        self.cmbBaudrate.setCurrentText(self.m_param['baudrate'])
        self.cmbByteSize.setCurrentText(self.m_param['bytesize'])
        self.cmbStopBits.setCurrentText(self.m_param['stopbits'])
        self.cmbParity.setCurrentText(self.m_param['parity'])

        if self.m_param['hexshow'] == 'True':
            self.chkHexShow.setChecked(True)
        else:
            self.chkHexShow.setChecked(False)

        if (self.m_param['hexsend'] == 'True'):
            self.chkHexSend.setChecked(True)
        else:
            self.chkHexSend.setChecked(False)

        self.linTimeNum.setText(self.m_param['timenum'])
        self.txtSendMsg.setPlainText(self.m_param['sendmsg'])
        self.txtRecvMsg.setPlainText("")

        self.m_callback = int(self.m_param['callback'])
        self.m_recvsize = int(self.m_param['recvsize'])
        self.m_recvetx = int(self.m_param['recvetx'])

    def paramFromUI(self):
        """
        parameter from UI.
        """
        self.m_param['port'] = self.cmbPort.currentText()
        self.m_param['baudrate'] = self.cmbBaudrate.currentText()
        self.m_param['bytesize'] = self.cmbByteSize.currentText()
        self.m_param['stopbits'] = self.cmbStopBits.currentText()
        self.m_param['parity'] = self.cmbParity.currentText()

        self.m_param['hexshow'] = str(self.chkHexShow.isChecked())
        self.m_param['hexsend'] = str(self.chkHexSend.isChecked())

        self.m_param['timenum'] = self.linTimeNum.text()
        self.m_param['sendmsg'] = self.txtSendMsg.toPlainText()
        # print(m_param)

    def readParamFromFile(self, file, sect):
        """
        read parameter from file.
        """
        f = configparser.ConfigParser()
        f.read(file)
        # s = f.sections()
        # print(s)

        self.m_param = dict(f.items(sect))
        print(self.m_param)
        # print(len(self.m_param))

    def writeParamToFile(self, file, sect):
        """
        write parameter to file.
        """
        f = configparser.ConfigParser()
        f.add_section(sect)

        for (key, value) in self.m_param.items():
            f.set(sect, key, value)
            # print(key + ':' + value)
        f.write(open(file, 'w'))

    def bytesToStr(self, argvbytes, hexformat):
        """
        byte to string.
        hex   input = b'x01\x02\x80\x00\xAA\xFF'  output = '01 02 80 00 AA FF'
        ascii input = b'01 02 03 04 05'           output = '01 02 03 04 05'
        """
        msg = bytes(argvbytes)
        if hexformat:
            s = ""
            for i in range(len(msg)):
                hhex = "%02x" % msg[i]
                s += hhex + ' '
            return s
        else:
            return msg.decode("utf-8")

    def bytesFromStr(self, argvstr, hexformat):
        """
        byte to string.
        hex   input = '01 02 80 00 AA FF'  output = b'x01\x02\x80\x00\xAA\xFF'
        ascii input = '01 02 03 04 05'     output = b'01 02 03 04 05'
        """
        msg = str(argvstr).strip()
        if len(msg) == 0:
            QMessageBox.information(self, "警告", "请输入字符后，再发送！", QMessageBox.Ok)
            return ""

        if hexformat:
            m = []
            m = msg.split()  # 以空格为分隔符分隔字符串，并存入list列表中
            s = ""
            for i in range(len(m)):
                if len(m[i]) < 2:
                    m[i] = '0' + m[i]
                s += m[i]

            # 到这一步时字符已经被处理为: '01028000AAFF'
            # 通过decode("hex")进行处理后的数据就是两个字符为一组的十进制数据
            # 进行异常处理，当进行数据格式转换时，因为可能有很多种情况导致转换失败，所以此处使用异常处理
            try:
                return codecs.decode(s, "hex_codec")
            except ValueError:
                QMessageBox.information(self, "警告", "请输入十六进制字符!", QMessageBox.Ok)
                return ""
        else:
            return msg.encode("utf-8")

    def openSerial(self):
        """
        open serial.
        """
        try:
            self.m_serial.port = self.cmbPort.currentText()
            self.m_serial.baudrate = int(self.cmbBaudrate.currentText())
            self.m_serial.stopbits = int(self.cmbStopBits.currentText())
            self.m_serial.bytesize = int(self.cmbByteSize.currentText())
            self.m_serial.parity = self.cmbParity.currentText()[:1]

            self.m_serial.open()

            if self.m_serial.is_open == True:
                self.serialThread = RecvThread(self.m_serial, self.showRecvMsg)
                self.serialThread.start()
                self.updateUI()

        except Exception:
            QMessageBox.information(self, "警告", "打开串口失败", QMessageBox.Ok)
            return

    def closeSerial(self):
        """
        close serial.
        """
        if self.m_serial.is_open == True:
            self.m_serial.close()
            self.serialThread.quit()
            self.updateUI()

    def showCount(self, num):
        self.lblRecvCnt.setText("R:%-10i" % num[0])
        self.lblSendCnt.setText("S:%-10i" % num[1])

    def parseRecvMsg(self, recvmsg):
        """
        parse receive message.
        """
        msg = str(recvmsg)
        m = []
        m = msg.strip().split()  # 以空格为分隔符分隔字符串，并存入list列表中
        # print(msg)
        if self.m_recvsize == len(m) or self.m_recvetx == int(m[-1]):
            time.sleep(0.01)
            self.on_manualSend_clicked()
            return

    def showRecvMsg(self, recvmsg):
        """
        show receive message.
        msg = b'01 02 03 04 05' or b'x01\x02\x80\x00\xAA\xFF'
        """
        s = self.bytesToStr(recvmsg, self.chkHexShow.isChecked())
        self.txtRecvMsg.append(s)
        # self.txtRecvMsg.setPlainText(self.txtRecvMsg.toPlainText() + s)

        self.m_count[0] += len(s)
        self.showCount(self.m_count)

        if self.m_callback != 0:
            self.parseRecvMsg(msg)

    def timerSend(self):
        """
        timer send message.
        """
        if self.m_serial.is_open:
            if self.chkTimeSend.isChecked():
                self.on_manualSend_clicked()
                Timer(int(self.linTimeNum.text())/1000, self.timerSend).start()
        else:
            if self.chkTimeSend.isChecked():
                self.chkTimeSend.setChecked(False)

    def on_openPort_clicked(self):
        if self.m_serial.is_open:
            self.closeSerial()
        else:
            self.openSerial()

    def on_clearWin_clicked(self):
        # s = "01 02 03 04"
        # self.txtRecvMsg.setPlainText(self.txtRecvMsg.toPlainText() + s)
        # return
        self.txtRecvMsg.clear()
        self.m_count = [0, 0]
        self.showCount(self.m_count)

    def on_saveWin_clicked(self):
        s = str(datetime.now())  # 2019-08-16 08:02:16.120510
        with open(LOG_FILE_PATH + s.replace(':', "") + ".txt", "w") as f:
            f.write(self.txtRecvMsg.toPlainText())

    def on_manualSend_clicked(self):
        if self.m_serial.is_open == False:
            QMessageBox.information(self, "警告", "请先打开串口!", QMessageBox.Ok)
            return

        s = self.bytesFromStr(self.txtSendMsg.toPlainText(), self.chkHexSend.isChecked())
        if s != "":
            self.m_serial.write(s)
            self.m_count[1] += len(s)
            self.showCount(self.m_count)

    def on_close_clicked(self):
        self.paramFromUI()
        self.writeParamToFile(TOOLS_FILE_NAME, TOOLS_SECT_NAME)  # save parameter
        self.closeSerial()
        self.close()

    def on_timeSend_clicked(self):
        self.timerSend()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
