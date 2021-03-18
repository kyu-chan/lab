import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import datetime
import pandas as pd
from pandas import Series, DataFrame


class Kiwoom:
    def __init__(self):
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")  ##ocx 객체 생성
        self.ocx.OnEventConnect.connect(self._handler_login)
        self.ocx.OnReceiveTrData.connect(self._handler_tr)  ## tr처리, 객체 생성해놔야함
        self.ocx.OnReceiveChejanData.connect(self._handler_chejan)
        self.ocx.OnReceiveMsg.connect(self._handler_msg)

    def GetLoginInfo(self, tag):
        data = self.ocx.dynamicCall("GetLoginInfo(QString)", tag)
        return data

    def CommConnect(self):
        self.ocx.dynamicCall("CommConnect()")
        self.login_loop = QEventLoop()  ##Qt코어부터
        self.login_loop.exec()

    def _handler_login(self):
        self.login_loop.exit()

    def GetCodeListByMarket(self, market):  ##종목코드받기
        data = self.ocx.dynamicCall("GetCodeListByMarket(QString)", market)  ##0은 장내, 8 etf, 10 코스닥
        codes = data.split(";")
        return codes[:-1]

    def GetMasterCodeName(self, code):  ## 코드주면 이름 뱉어
        data = self.ocx.dynamicCall("GetMasterCodeName(QString)", code)
        return data

    def GetMasterListedStockCnt(self, code):  ##유동주식수
        data = self.ocx.dynamicCall("GetMasterListedStockCnt(QString)", code)
        return data

    def GetMasterListedStockDate(self, code):
        data = self.ocx.dynamicCall("GetMasterListedStockDate(QString)", code)
        return data

    def GetMasterLastPrice(self, code):  ## 직전일 종가
        data = self.ocx.dynamicCall("GetMasterLastPrice(QSting)", code)
        return int(data)

    def GetMasterConstruction(self, code):  ##감리구분
        data = self.ocx.dynamicCall("GetMasterConstruction(QString)", code)
        return data

    def GetMasterStockState(self, code):  ##종목상태
        data = self.ocx.dynamicCall("GetMasterStockState(QStirng)", code).split('|')
        return data

    ####테마, 섹터
    def GetThemeGroupList(self, type):  ### 0 or 1을 받는다.
        data = self.ocx.dynamicCall("GetThemeGroupList(int)", type)  ##int로 input
        tokens = data.split(';')

        data_dic = {}
        for theme in tokens:
            code, name = theme.split('|')
            if type == 0:
                data_dic[code] = name
            else:
                data_dic[name] = code

        return data_dic  ### 테마 그룹과 테마 번호가 어떻게 구성되었는지 받아온다.
        ## pprint로 출력하면 더 가독성이 좋다.

    def GetThemeGroupCode(self, theme_code):  ##테마번호 넣으면 거기 속하는 종목을 뱉는다.
        data = self.ocx.dynamicCall("GetThemeGroupCode(QString)", theme_code)
        tokens = data.split(';')

        result = []
        for code in tokens:  ### 코드를 A000000 이런식으로 영어하나 달고 나온다.
            result.append(code[1:])

        return result

    def SetInputValue(self, item, value):  ## 종목코드와 그 값을 받아  ### setting을 하는거지 반환하는게 아님
        self.ocx.dynamicCall("SetInputValue(QString,QString)", item, value)

    def CommRqData(self, rqname, trcode, next, screen):  ##서버에 요청,  Api 설명서 참조하면서 변경해가며
        self.ocx.dynamicCall("CommRqData(QString,QString,int,QString)", rqname, trcode, next, screen)
        self.tr_loop = QEventLoop()  ##요청하고 대기해야하니 이벤트루프
        self.tr_loop.exec()  ##여기서 생김

    def _handler_login(self, err):
        self.login_loop.exit()

    def GetCommData(self, trcode, rqname, index, item):  ##데이터 가져오기 시작
        data = self.ocx.dynamicCall("GetCommData(QString,QString,int,QString)", trcode, rqname, index, item)
        return data.strip()  ## 좌우공백 있을수가 있어서

    def GetRepeatCnt(self, trcode, rqname):  ##멀티데이터 리퀘스트,  몇 개(로우)로 구성되는지
        ret = self.ocx.dynamicCall("GetRepeatCnt(QString,QString)", trcode, rqname)
        return ret

    def _handler_tr(self, screen, rqname, trcode, record, next):  ###요청하는 tr이 뭔지에 따라 여기 조작필요
        if next == '2':
            self.remained = True
        else:
            self.remained = False
#        self.tr_data = {}  ##미리 self에 딕셔너리 하나 만들어놓고
#
#        per = self.GetCommData(trcode, rqname, 0, "PER")  ### 0은 지금같은경우 데이터가 1차원인데 ROW인덱스
#        pbr = self.GetCommData(trcode, rqname, 0, "PBR")
#        self.tr_data['PER'] = per
#        self.tr_data['PBR'] = pbr

        if rqname == "opt10081":  ## 한번에 600개씩 오니까 데이터가 600개보다 많을때는 연속조회를 해줘야하는데
            ## sPreNext값에 2를 줘서 연속으로 받아온다.
            self._opt10081(rqname, trcode)

        try:
            self.tr_loop.exit()

        except:
            pass


    ###일봉데이터 tr
    def _opt10081(self, rqname, trcode):
        data = []
        columns = ["시가","고가","저가","종가","거래량"]
        index = []
        rows = self.GetRepeatCnt(trcode, rqname)

        for i in range(rows):
            date = self.GetCommData(trcode, rqname, i, "일자")
            open = self.GetCommData(trcode, rqname, i, "시가")
            high = self.GetCommData(trcode, rqname, i, "고가")
            low = self.GetCommData(trcode, rqname, i, "저가")
            close = self.GetCommData(trcode, rqname, i, "현재가")
            volume = self.GetCommData(trcode, rqname, i, "거래량")

            dt = datetime.datetime.strptime(date, "%Y%m%d")
            index.append(dt)
            data.append((open, high, low, close, volume))

        self.tr_data = DataFrame(data=data, index=index, columns=columns)


    def SendOrder(self, rqname, screen, accno, order_type, code, quantity, price, hoga, order_no):
        self.ocx.dynamicCall("SendOrder(QString,QString,QString,int,QString,int,int,QString,QString",
                             [rqname, screen, accno, order_type, code, quantity, price, hoga, order_no])
        ###인자가 8개이상이면 리스트로 넘겨줘야함
        ##이벤트루프는 필요할때 쓰는데 시장가같으면 필요없겠지
        self.order_loop = QEventLoop()
        self.order_loop.exec()

    def _handler_chejan(self, gubun, item_cnt, fid_list):
        print("OnReceiveChejanData", gubun, item_cnt, fid_list)

    def _handler_msg(self, screen, rqname, trcode, msg):
        print("OnReceiveMsg", screen,rqname,trcode, msg)
    

app = QApplication(sys.argv)
