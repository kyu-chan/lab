from kiwoom import *
import time
import pandas as pd

kiwoom = Kiwoom()
kiwoom.CommConnect()
print('정상')
codes = kiwoom.GetCodeListByMarket('0') + kiwoom.GetCodeListByMarket('10')
len(codes)
#### PER로 스크리닝해보자
per_result = []
for code in codes:  ## 50종목선택
    kiwoom.SetInputValue("종목코드", code)
    kiwoom.CommRqData("opt10001", "opt10001", 0, "0101")  ## 연속조회, 회면번호

    per = kiwoom.tr_data['PER']
    pbr = kiwoom.tr_data['PBR']

    try:
        per = float(per)    ##문자열로 오니까 바꿔주는데 데이터가 없는 경우나 에러가나는 경우 제거
    except:
        per = 0
    try:
        pbr = float(pbr)
    except:
        pbr = 0

    ##스크리닝
    if 2.5 <= per <= 15:
        per_result.append((kiwoom.GetMasterCodeName(code), per, pbr))

    time.sleep(1)


### PBR기준으로 정렬
result = sorted(per_result, key= lambda x:x[2])   ##오름차순으로 , sort는 원본을 헤치지않기위해, sort()랑 다르게 ascending이 아닐
                                                 ## reverse =True로 내림차순가능
data = []
for i in result:
    name = i[0]
    per  = i[1]
    pbr  = i[2]

    data.append(name, per, pbr)

df = pd.DataFrame(data=data, columns=['종목명', 'PER', 'PBR']).set_index('종목명')

df.to_excel("PER_PBR_sort.xlsx")

