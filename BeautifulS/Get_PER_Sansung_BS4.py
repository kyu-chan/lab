import requests
from bs4 import BeautifulSoup


#url = "https://finance.naver.com/item/main.nhn?code=005930"
#resp = requests.get(url)

codes = ["005930", "066570", "000660"]

# def get_per(code):
#  ~~~~~로 함수형태로 사용도 호출로 바로 사용할 수 있으니 프로젝트 진행시 구현해볼것

#bs = BeautifulSoup(resp.text, "html5lib")
#print(type(bs))
sel = "#_per"

#tab_con1 > div:nth-child(5)
#result = bs.select(sel)
for code in codes:
    url = f"https://finance.naver.com/item/main.nhn?code={code}"
    resp = requests.get(url)
    bs = BeautifulSoup(resp.text, "html5lib")
    result = bs.select(sel)
    for item in result:
        print(code, item.text)
