import socket
from desktop import *
from single_game import *
from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5 import sip
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap
from login import Ui_login
from register import Ui_register
import gc
import random
import time
import sys
import os
import struct
import json

WIDTH = 1000
HEIGHT = 800
TITLE = "曲奇五子棋"

ADDRESS = "qqof.hcolda.com"
PORT = 11451

# 全局socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class receive_thread(QThread):
    # 接收信息系统，在连接之后才创建
    msglist = list()
    receivemsg = bytes()
    can_get = 0

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            try:
                self.receivemsg += s.recv(1024)
                # print(self.receivemsg)
                head = self.receivemsg[:8]
                head = struct.unpack("Q", head)[0]
                if (len(self.receivemsg[8:]) >= head):
                    self.msglist.append(self.receivemsg[8:8+head])
                    self.receivemsg = self.receivemsg[8+head:]
                    self.can_get += 1
            except:
                time.sleep(0.1)

    def get_msg(self):
        # 获取解包后的信息
        while True:
            try:
                if (self.can_get > 0):
                    msg = self.msglist.pop(0)
                    self.can_get -= 1
                    return msg
            except:
                pass
            time.sleep(0.01)


def sendmsg(string: bytes):
    s.send(struct.pack("Q", len(string))+string)


def receivemsg() -> bytes:
    return receive_system.get_msg()


class connect_babel(QThread):
    def __init__(self, label: QLabel):
        super().__init__()
        self.label = label
        self.num = 0

    def run(self):
        while True:
            self.label.setStyleSheet("color:black")
            self.label.setText("正在连接服务器{}".format('.'*self.num))
            self.num += 1
            if (self.num > 3):
                self.num = 0
            time.sleep(1)


class connect(QThread):
    signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.open = False

    def run(self) -> None:
        global s
        socket.setdefaulttimeout(5)
        for i in range(3):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ADDRESS, PORT))
                s.send(struct.pack("Q", len(json.dumps({"is_on": {}}, ensure_ascii=False).encode(
                    'gb18030')))+json.dumps({"is_on": {}}, ensure_ascii=False).encode('gb18030'))
                if (json.loads(s.recv(1024)[8:])["is_on"]):
                    self.open = True
                    break
            except:
                pass
        if (self.open):
            s.close()
            socket.setdefaulttimeout(None)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ADDRESS, PORT))
            self.signal.emit(True)
            return
        else:
            s.close()
            socket.setdefaulttimeout(None)
            self.signal.emit(False)
            return


class login_class(Ui_login, QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('登录')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.label.setPixmap(QPixmap("./library/main/login_bg.png"))
        self.label_2.setPixmap(
            QPixmap("./library/bgs/{}.png".format(random.randint(1, 4))))
        self.pushButton.clicked.connect(self.Close)
        self.pushButton_2.clicked.connect(self.showMinimized)
        self.pushButton_3.setDisabled(True)
        self.pushButton_4.setDisabled(True)
        self.pushButton_5.setVisible(False)
        self.pushButton_5.clicked.connect(self.reconnect)
        self.pushButton_3.clicked.connect(self.login)
        self.pushButton_4.clicked.connect(self.register)
        if "library" not in os.listdir():
            os.mkdir("library")
            if "data" not in os.listdir("./library"):
                os.mkdir("./library/data")
        if ("password.json" in os.listdir('./library/data')):
            try:
                f = open('./library/data/password.json', 'r')
                data = json.load(f)
                f.close()
                global username, password
                if (data["is_on"]):
                    username = data["username"]
                    password = data['password']
                    self.checkBox.setChecked(True)
                    self.lineEdit.setText(data["username"])
                    self.lineEdit_2.setText(data['password'])
                else:
                    username = ''
                    password = ''
            except:
                f = open('./library/data/password.json', 'w')
                f.close()
        else:
            f = open('./library/data/password.json', 'w')
            f.close()

        self.start_conn()

    def start_conn(self):
        self.connect_thr = connect_babel(self.label_8)
        self.connect = connect()
        self.connect.signal.connect(self.conn)
        self.connect.start()
        self.connect_thr.start()

    def conn(self, bo: bool):
        if (bo):
            self.connect_thr.terminate()
            self.label_8.setStyleSheet("color:green")
            self.label_8.setText("成功连接服务器！")
            self.pushButton_3.setDisabled(False)
            self.pushButton_4.setDisabled(False)
            global receive_system
            receive_system = receive_thread()
            receive_system.start()
        else:
            self.connect_thr.terminate()
            self.label_8.setStyleSheet("color:red")
            self.label_8.setText("无法连接服务器！")
            self.pushButton_5.setVisible(True)

    def reconnect(self):
        self.pushButton_5.setVisible(False)
        self.start_conn()

    def Close(self):
        os._exit(0)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos()-self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos()-self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False

    def login(self):
        if (len(self.lineEdit.text().strip()) == 0 or len(self.lineEdit_2.text().strip()) == 0):
            QMessageBox.warning(self, "警告", "账号或密码没有填完整！")
            return
        global username, password, game_
        sendmsg(json.dumps({"login": {"name": self.lineEdit.text().strip(
        ), "password": self.lineEdit_2.text().strip()}}, ensure_ascii=False).encode('gb18030'))
        msg = json.loads(receivemsg().decode('gb18030'))
        if ("error" in list(msg["login"].keys())):
            QMessageBox.warning(self, "警告", msg["login"]['error'])
            return
        username = self.lineEdit.text().strip()
        password = self.lineEdit_2.text().strip()
        if self.checkBox.isChecked():
            with open('./library/data/password.json', 'w') as f:
                json.dump({"is_on": True, "username": username,
                          'password': password}, f)
        else:
            with open('./library/data/password.json', 'w') as f:
                json.dump({"is_on": True, "username": '', 'password': ''}, f)
        self.game_ = main_desk(s, username, receive_system)
        self.close()
        # sip.delete(self)
        run()

    def register(self):
        global register_class_sy
        register_class_sy = register_class()
        register_class_sy.show()
        register_class_sy.signal.connect(self.show)
        self.close()


class register_class(Ui_register, QWidget):
    signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('登录')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.label.setPixmap(QPixmap("./library/main/login_bg.png"))
        self.label_2.setPixmap(
            QPixmap("./library/bgs/{}.png".format(random.randint(5, 7))))

        self.pushButton.clicked.connect(self.Close)
        self.pushButton_2.clicked.connect(self.showMinimized)
        self.pushButton_4.clicked.connect(self.login)
        self.pushButton_3.clicked.connect(self.register)

    def login(self):
        self.close()
        self.signal.emit()
        sip.delete(self)

    def Close(self):
        os._exit(0)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos()-self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos()-self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False

    def register(self):
        if (len(self.lineEdit.text().strip()) == 0 or len(self.lineEdit_2.text().strip()) == 0 or len(self.lineEdit_2.text().strip()) == 0):
            QMessageBox.warning(self, "警告", "有空没有填!")
            return
        if (self.lineEdit_3.text().strip() != self.lineEdit_2.text().strip()):
            QMessageBox.warning(self, "警告", "密码不一致!")
            return
        if (len(self.lineEdit_2.text().strip()) < 6):
            QMessageBox.warning(self, "警告", "密码太短!")
            return
        sendmsg(json.dumps({"register": {"name": self.lineEdit.text().strip(
        ), "password": self.lineEdit_2.text().strip()}}, ensure_ascii=False).encode('gb18030'))
        msg = json.loads(receivemsg().decode('gb18030'))
        if ("success" in list(msg["register"].keys())):
            QMessageBox.information(self, "信息", "注册成功!")
            self.login()
        else:
            QMessageBox.warning(self, "警告", msg["register"]['error'])


class gcthread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            gc.collect(2)
            time.sleep(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    thr = gcthread()
    thr.start()
    main_ = login_class()
    main_.show()
    sys.exit(app.exec_())
