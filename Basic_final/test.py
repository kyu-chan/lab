from kiwoom import *
import pickle


f = open("data.db", "rb")   ##얘는 읽고 주문 넣으면 되니까  r : 리드모드로 가져와
codes = pickle.load(f)   ## 아까 list로 저장했으니 pickle은 list로 읽어온다
f.close()    ## open을 했으면 항상 close하는 습관
print(codes)