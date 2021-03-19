from kiwoom import *

kiwoom = Kiwoom()
kiwoom.CommConnect()
print("정상접속")

kiwoom.GetConditionLoad()
#condition = kiwoom.GetConditionNameList()
#print(condition)

kiwoom.SendCondition("0101", "01_try", "000", 0)
print(kiwoom.condition_codes)