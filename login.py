# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_login(object):
    def setupUi(self, login):
        login.setObjectName("login")
        login.setEnabled(True)
        login.resize(709, 468)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(login.sizePolicy().hasHeightForWidth())
        login.setSizePolicy(sizePolicy)
        self.label = QtWidgets.QLabel(login)
        self.label.setGeometry(QtCore.QRect(0, 0, 701, 461))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../main/login_bg.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(login)
        self.pushButton.setGeometry(QtCore.QRect(660, 10, 16, 16))
        self.pushButton.setStyleSheet("QPushButton{\n"
"    color:White;\n"
"    border-radius: 7px;\n"
"    font-family:微软雅黑;\n"
"    background:#FF0000;\n"
"    border:7px;\n"
"}\n"
"QPushButton:hover{\n"
"    background:#BC1717;\n"
"}\n"
"QPushButton:pressed{\n"
"    background:#BC1717;\n"
"}")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(login)
        self.pushButton_2.setGeometry(QtCore.QRect(630, 10, 16, 16))
        self.pushButton_2.setStyleSheet("QPushButton{\n"
"    color:White;\n"
"    border-radius: 7px;\n"
"    font-family:微软雅黑;\n"
"    background:#C0C0C0;\n"
"    border:7px;\n"
"}\n"
"QPushButton:hover{\n"
"    background:#A8A8A8;\n"
"}\n"
"QPushButton:pressed{\n"
"    background:#A8A8A8;\n"
"}")
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(login)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 411, 461))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("../bgs/1.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_6 = QtWidgets.QLabel(login)
        self.label_6.setGeometry(QtCore.QRect(510, 210, 141, 16))
        self.label_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.pushButton_3 = QtWidgets.QPushButton(login)
        self.pushButton_3.setGeometry(QtCore.QRect(470, 280, 101, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("QPushButton{\n"
"    color:White;\n"
"    border-radius: 15px;\n"
"    font: \"站酷高端黑\";\n"
"    background:#008B8B;\n"
"    border:15px;\n"
"}\n"
"QPushButton:hover{\n"
"    background:#00CED1;\n"
"}\n"
"QPushButton:pressed{\n"
"    background:#00CED1;\n"
"}")
        self.pushButton_3.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_3.setCheckable(False)
        self.pushButton_3.setAutoRepeat(False)
        self.pushButton_3.setAutoExclusive(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.checkBox = QtWidgets.QCheckBox(login)
        self.checkBox.setGeometry(QtCore.QRect(570, 240, 71, 16))
        self.checkBox.setObjectName("checkBox")
        self.label_5 = QtWidgets.QLabel(login)
        self.label_5.setGeometry(QtCore.QRect(510, 160, 141, 16))
        self.label_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_3 = QtWidgets.QLabel(login)
        self.label_3.setGeometry(QtCore.QRect(450, 140, 31, 31))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(":/user.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.pushButton_4 = QtWidgets.QPushButton(login)
        self.pushButton_4.setGeometry(QtCore.QRect(590, 280, 61, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("QPushButton{\n"
"    color:White;\n"
"    border-radius: 15px;\n"
"    font: \"站酷高端黑\";\n"
"    background:#008B8B;\n"
"    border:15px;\n"
"}\n"
"QPushButton:hover{\n"
"    background:#00CED1;\n"
"}\n"
"QPushButton:pressed{\n"
"    background:#00CED1;\n"
"}")
        self.pushButton_4.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.label_4 = QtWidgets.QLabel(login)
        self.label_4.setGeometry(QtCore.QRect(450, 190, 31, 31))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap(":/logsure.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.label_7 = QtWidgets.QLabel(login)
        self.label_7.setGeometry(QtCore.QRect(510, 160, 141, 16))
        self.label_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(login)
        self.label_8.setGeometry(QtCore.QRect(430, 410, 151, 31))
        self.label_8.setStyleSheet("color:red")
        self.label_8.setObjectName("label_8")
        self.pushButton_5 = QtWidgets.QPushButton(login)
        self.pushButton_5.setGeometry(QtCore.QRect(590, 410, 61, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet("QPushButton{\n"
"    color:White;\n"
"    border-radius: 15px;\n"
"    font: \"站酷高端黑\";\n"
"    background:#008B8B;\n"
"    border:15px;\n"
"}\n"
"QPushButton:hover{\n"
"    background:#00CED1;\n"
"}\n"
"QPushButton:pressed{\n"
"    background:#00CED1;\n"
"}")
        self.pushButton_5.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_5.setObjectName("pushButton_5")
        self.label_9 = QtWidgets.QLabel(login)
        self.label_9.setGeometry(QtCore.QRect(10, 419, 221, 31))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("color:white")
        self.label_9.setObjectName("label_9")
        self.lineEdit = QtWidgets.QLineEdit(login)
        self.lineEdit.setGeometry(QtCore.QRect(510, 140, 141, 31))
        self.lineEdit.setAutoFillBackground(False)
        self.lineEdit.setStyleSheet("")
        self.lineEdit.setInputMask("")
        self.lineEdit.setText("")
        self.lineEdit.setFrame(False)
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setReadOnly(False)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(login)
        self.lineEdit_2.setGeometry(QtCore.QRect(510, 190, 141, 31))
        self.lineEdit_2.setAutoFillBackground(False)
        self.lineEdit_2.setInputMask("")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setFrame(False)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label.raise_()
        self.lineEdit.raise_()
        self.lineEdit_2.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.label_2.raise_()
        self.label_6.raise_()
        self.pushButton_3.raise_()
        self.checkBox.raise_()
        self.label_5.raise_()
        self.label_3.raise_()
        self.pushButton_4.raise_()
        self.label_4.raise_()
        self.label_7.raise_()
        self.label_8.raise_()
        self.pushButton_5.raise_()
        self.label_9.raise_()

        self.retranslateUi(login)
        QtCore.QMetaObject.connectSlotsByName(login)

    def retranslateUi(self, login):
        _translate = QtCore.QCoreApplication.translate
        login.setWindowTitle(_translate("login", "Form"))
        self.pushButton_3.setText(_translate("login", "登录"))
        self.checkBox.setText(_translate("login", "记住密码"))
        self.pushButton_4.setText(_translate("login", "注册"))
        self.label_8.setText(_translate("login", "无法连接至服务器！"))
        self.pushButton_5.setText(_translate("login", "重连"))
        self.label_9.setText(_translate("login", "@制作者：曲奇Onfree"))
        self.lineEdit.setPlaceholderText(_translate("login", "账号"))
        self.lineEdit_2.setPlaceholderText(_translate("login", "密码"))
import login_rc
