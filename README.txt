

3. ��������
3.1 ��ť�¼�����
��ťֻ����һ�Σ����ǻ���ֵ���3�ΰ�ť�¼�������
��ť����ΪbtnClearWin�������¼�������£�
self.btnClearWin.clicked.connect(self.on_btnClearWin_clicked)
���⵱ȡ���˰�ť�Ĺ����¼����󣬵����ťʱ�Ի���ô˹������������ҵ����¼���3�α����2�Ρ�

�������¼��ĺ������Ƹ�Ϊ�������ʱ������
self.btnClearWin.clicked.connect(self.on_clearWin_clicked)

��������btnClearWin��ť�Ĺ����¼������������ƺ�PyQt5Ĭ�ϵİ�ť�¼�����(on_btnClearWin_clicked)��ͬʱ����ֵ���3�ΰ�ť�¼�������

3.2 textedit��ʾ����
��showRecvMsg�����У���ʾtextedit����ʱ����ʹ��append()����ʱû�����⣬ʹ��setPlainText()����ʱ������ִ���
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

�ڰ�ť�Ĺ����¼�����setPlainText()������ʾtextedit����ʱ������
def on_clearWin_clicked(self):
    s = "01 02 03 04"
    self.txtRecvMsg.setPlainText(self.txtRecvMsg.toPlainText() + s)
    return

��PyQt5��plain text eidt��ʾ��������ʱ��������һ����

������û�н�������һ���о���
