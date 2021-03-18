import sys
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


import pyupbit
import datetime



class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.dynamicCall("CommConnect()")
        self.ocx.OnEventConnect.connect(self.handle_login)


        self.resize(400,300)
        self.move(700,300)
        self.setWindowTitle("자동매매 프로그램")
        self.label = QLabel("비트코인  : ", self)
        self.label.move(10,10)

        icon = QIcon("icon.png")
        self.setWindowIcon(icon)

        self.list_widget = QListWidget(self)
        self.list_widget.resize(250,280)
        self.list_widget.move(10,10)

        self.line_edit = QLineEdit(self)
        self.line_edit.move(270,130)
        self.line_edit.resize(100, 30)

        self.timer = QTimer()
        self.timer.start(1000)   ##1000이 1초
        self.timer.timeout.connect(self.handle_timer)

        self.btn_login = QPushButton("로그인 정보", self)
        self.btn_login.move(270,130)
        self.btn_login.clicked.connect(self.handle_btn_login_clicked)

        self.btn_add = QPushButton("추가", self)
        self.btn_add.move(270,10)

        self.btn_reset = QPushButton("초기화", self)
        self.btn_reset.move(270,50)

        self.btn_buy = QPushButton("매수", self)
        self.btn_buy.move(270,90)
        self.btn_buy.clicked.connect(self.btn_clicked_buy)

        self.btn_reset.clicked.connect(self.btn_reset_clicked)
        self.btn_add.clicked.connect(self.btn_add_clicked)

    def handle_login(self, login_status):
        if login_status == 0:
            self.statusBar().showMessage("로그인 성공")
        else:
            self.statusBar().showMessage("로그인 실패")

    def handle_btn_login_clicked(self):
        account_nums = self.ocx.dynamicCall("GetLoginInfo(QString)", "ACCNO")
        User_Id = self.ocx.dynamicCall("GetLoginInfo(QString)", "USER_ID")
        User_Name = self.ocx.dynamicCall("GetLoginInfo(QString)", "USER_NAME")
        print(account_nums)
        print(User_Id)
        print(User_Name)

    def btn_reset_clicked(self):
        self.list_widget.clear()

    def btn_add_clicked(self):
        self.list_widget.addItem("데이터")


    def handle_timer(self):
        btc = pyupbit.get_current_price("KRW-BTC")
        self.line_edit.setText(str(btc))
        now = datetime.datetime.now()
        self.statusBar().showMessage(str(now))


    def btn_clicked_buy(self):
        self.line_edit.setText("매수")


app = QApplication(sys.argv)
win = MyWindow()
win.show()
app.exec_()