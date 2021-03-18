from kiwoom import *


kiwoom = Kiwoom()
kiwoom.CommConnect()
print("정상")

kiwoom.SetInputValue("종목코드", "005930")
kiwoom.SetInputValue("기준일자", "20210318")
kiwoom.SetInputValue("수정주가구분", 1)
kiwoom.CommRqData("opt10081","opt10081",0,"0101") ## 첫번재 input이 리퀘스트 이름인데 이전 wrapper에서 이렇게 해놓음
kiwoom.tr_data.to_excel("samsung.xlsx")




