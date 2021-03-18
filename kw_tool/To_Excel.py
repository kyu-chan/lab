from kiwoom import *
import pandas as pd
from datetime import datetime
import time

kiwoom = Kiwoom()
kiwoom.CommConnect()
print("로그인")

kospi = kiwoom.GetCodeListByMarket('0')
kosdaq = kiwoom.GetCodeListByMarket('10')
codes = kospi + kosdaq

data = []

for code in codes:
    name = kiwoom.GetMasterCodeName(code)
    os_Cnt = kiwoom.GetMasterListedStockCnt(code)/10000
    Suv_days = (datetime.today().year - int(kiwoom.GetMasterListedStockDate(code)[0:4]))*365 \
               + (datetime.today().month - int(kiwoom.GetMasterListedStockDate(code)[4:6]))*30 \
               +(datetime.today().day - int(kiwoom.GetMasterListedStockDate(code)[6:]))

    if kiwoom.GetMasterConstruction(code) == '정상':
        const = ' '
    else:
        const = kiwoom.GetMasterConstruction(code)

    if ('거래정지' or '관리종목' or '투자유의종목') in kiwoom.GetMasterStockState(code):
        S_state = '제외'
    else:
        S_state = ' '


    data.append((code, name, os_Cnt, Suv_days, const, S_state))




df = pd.DataFrame(data=data, columns=['code', '종목명', '유동주식 수(만)', '상장후 운영일수',
                                      '감리유의', '상태유의']).set_index('code')
## 서버에서 PER, PBR을 일일이 요청하다보니 시간이 너무 많이 걸린다 -> 크롤링이나 웹스크래핑으로 데이터 수집하는게 더 빠를듯
df.to_excel("code.xlsx")

