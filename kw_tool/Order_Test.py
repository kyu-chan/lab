from kiwoom import *

kiwoom = Kiwoom()
kiwoom.CommConnect()
print("정상")

accounts = kiwoom.GetLoginInfo("ACCNO")
account = accounts.split(';')[0]

kiwoom.SendOrder("Long", "0101", account, 1, "005930", 10, 0, "03","") # 1이 매수 2가 매도 (0, "03")은 시장가
