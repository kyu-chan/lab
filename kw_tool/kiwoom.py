import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *


class Kiwoom:
    def __init__(self):
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")   ##ocx 객체 생성
        self.ocx.OnEventConnect.connect(self._handler_login)

    def GetLoginInfo(self, tag):
        data = self.ocx.dynamicCall("GetLoginInfo(QString)", tag)
        return data

    def CommConnect(self):
        self.ocx.dynamicCall("CommConnect()")
        self.login_loop = QEventLoop()   ##Qt코어부터
        self.login_loop.exec()

    def _handler_login(self):
        self.login_loop.exit()


    def GetCodeListByMarket(self, market):   ##종목코드받기
        data = self.ocx.dynamicCall("GetCodeListByMarket(QString)", market) ##0은 장내, 8 etf, 10 코스닥
        codes =  data.split(";")
        return codes[:-1]

    def GetMasterCodeName(self, code):   ## 코드주면 이름 뱉어
        data = self.ocx.dynamicCall("GetMasterCodeName(QString)", code)
        return data

    def GetMasterListedStockCnt(self, code): ##유동주식수
        data = self.ocx.dynamicCall("GetMasterListedStockCnt(QString)", code)
        return data

    def GetMasterListedStockDate(self, code):
        data = self.ocx.dynamicCall("GetMasterListedStockDate(QString)", code)
        return data

    def GetMasterLastPrice(self, code): ## 직전일 종가
        data = self.ocx.dynamicCall("GetMasterLastPrice(QSting)", code)
        return int(data)

    def GetMasterConstruction(self, code):  ##감리구분
        data = self.ocx.dynamicCall("GetMasterConstruction(QString)", code)
        return data

    def GetMasterStockState(self, code):  ##종목상태
        data = self.ocx.dynamicCall("GetMasterStockState(QStirng)", code).split('|')
        return data

####테마, 섹터
    def GetThemeGroupList(self, type):   ### 0 or 1을 받는다.
        data = self.ocx.dynamicCall("GetThemeGroupList(int)", type)  ##int로 input
        tokens = data.split(';')

        data_dic = {}
        for theme in tokens:
            code, name = theme.split('|')
            if type == 0:
                data_dic[code] = name
            else:
                data_dic[name] = code

        return data_dic      ### 테마 그룹과 테마 번호가 어떻게 구성되었는지 받아온다.
                            ## pprint로 출력하면 더 가독성이 좋다.


    def GetThemeGroupCode(self, theme_code):   ##테마번호 넣으면 거기 속하는 종목을 뱉는다.
        data = self.ocx.dynamicCall("GetThemeGroupCode(QString)", theme_code)
        tokens = data.split(';')

        result = []
        for code in tokens:    ### 코드를 A000000 이런식으로 영어하나 달고 나온다.
            result.append(code[1:])

        return result






app = QApplication(sys.argv)
