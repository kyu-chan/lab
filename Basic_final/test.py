from kiwoom import *

kiwoom = Kiwoom()
kiwoom.CommConnect()



kiwoom.SendCondition("0101","02_Try", "001", 0)  ##마지막 0은 일반조회
codes = kiwoom.condition_codes
print(codes)