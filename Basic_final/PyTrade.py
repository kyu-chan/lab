from kiwoom import *
import pickle
import time

class PyTrader:

    def __init__(self):
        self.kiwoom = Kiwoom()   ##객체부터 생성
        self.kiwoom.CommConnect()  ##접속


    def run(self):   ## 데이터 db로 저장해놓은 것을 읽어서 주문 넣게
        accounts = self.kiwoom.GetLoginInfo("ACCNO")
        account = accounts.split(';')[0]

        ##파일
        try:
            f = open("data.db", "rb")   ##얘는 읽고 주문 넣으면 되니까  r : 리드모드로 가져와
            codes = pickle.load(f)   ## 아까 list로 저장했으니 pickle은 list로 읽어온다
            f.close()    ## open을 했으면 항상 close하는 습관

        except:
            codes = []

        ##long 주문
        for code in codes:
            self.kiwoom.SendOrder("Buy_M_O",
                                  "0101",
                                  account,
                                  1,   ##매수1
                                  code,
                                  10,  ## 주문수량
                                  0,   ## 시장가니까 금액 0으로
                                  "03",  ##시장가 03번
                                  "")   ##오더넘버 비우고 주문
            time.sleep(0.2)   ##초당 주문 횟수 제한때문에 슬립걸어줘야

if __name__ == "__main__":
    pytrader = PyTrader()
    pytrader.run()