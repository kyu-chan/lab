from kiwoom import *

kiwoom = Kiwoom()
kiwoom.CommConnect()
print("로그인")

cnt = kiwoom.GetCodeListByMarket("0")
print(cnt)
