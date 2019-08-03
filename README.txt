

3. 调试问题
3.1 按钮事件问题
按钮只按了一次，但是会出现调用3次按钮事件的现象。
按钮名称为btnClearWin，关联事件语句如下：
self.btnClearWin.clicked.connect(self.on_btnClearWin_clicked)
另外当取消此按钮的关联事件语句后，点击按钮时仍会调用此关联函数，并且调用事件由3次变成了2次。

当关联事件的函数名称改为如下语句时正常。
self.btnClearWin.clicked.connect(self.on_clearWin_clicked)

分析：当btnClearWin按钮的关联事件（函数）名称和PyQt5默认的按钮事件名称(on_btnClearWin_clicked)相同时会出现调用3次按钮事件的现象。

3.2 textedit显示问题
在showRecvMsg函数中，显示textedit数据时，当使用append()方法时没有问题，使用setPlainText()方法时程序出现错误。
def showRecvMsg(self, argvmsg):
    """
    show receive message.
    """
    msg = str(argvmsg)
    # print(msg)
    s = ""
    if self.chkHexShow.isChecked():
        for i in range(len(msg)):
            hval = ord(msg[i])
            hhex = "%02x" % hval
            s += hhex + ' '
    else:
        s = msg

    self.txtRecvMsg.append(s)
    # self.txtRecvMsg.setPlainText(self.txtRecvMsg.toPlainText() + s)

在按钮的关联事件中用setPlainText()方法显示textedit数据时正常。
def on_clearWin_clicked(self):
    s = "01 02 03 04"
    self.txtRecvMsg.setPlainText(self.txtRecvMsg.toPlainText() + s)
    return

用PyQt5的plain text eidt显示部件测试时故障现象一样。

此问题没有解决，需进一步研究。
