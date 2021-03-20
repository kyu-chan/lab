from kiwoom import *
from selenium import webdriver
import time
import pandas as pd

kiwoom = Kiwoom()
kiwoom.CommConnect()

codes = kiwoom.GetCodeListByMarket('0') + kiwoom.GetCodeListByMarket('10')
data = []

##창숨기기 옵션
options = webdriver.ChromeOptions()
options.add_argument("headless")

for code in codes:
    name = kiwoom.GetMasterCodeName(code)
    driver = webdriver.Chrome('chromedriver.exe', options=options)
    driver.get(f'https://finance.naver.com/item/main.nhn?code={code}')

    selector = "#_market_sum"
    ui = driver.find_element_by_css_selector(selector)
    data.append((name, ui.text))
    time.sleep(1)

df = pd.DataFrame(data=data, columns=['name','시총']).set_index('name')
## 서버에서 PER, PBR을 일일이 요청하다보니 시간이 너무 많이 걸린다 -> 크롤링이나 웹스크래핑으로 데이터 수집하는게 더 빠를듯
df.to_excel("test_01.xlsx")

### fnguide보면 정보를 새로운 창에서 제공하는데
### 기본적으로 webdriver는 메인창을 가르키고 있으므로 창 전환이 필요하겠지
### 창전환하는 스크래핑 연습도 필요

### 너무 느림 -> 이런 데이터는 증권사 api에 요청해서 받는 형태가 훨씬 빠르겠음
