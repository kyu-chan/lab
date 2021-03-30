## 웹페이지 구성에 있어, Get , Post , 웹 분석
## Get은 데이터를 url에 포함하므로 데이터 길이에 제한
## post는 데이터를 url에 포함하지 않고 숨겨서 전달하므로 제약을 좀 덜 받음
## Get을 사용하는 정적페이지는 페이지가 변화하면 url도 변하구나

import requests
from bs4 import BeautifulSoup

url = "https://www.google.co.kr/search?q=퀀트"
resp = requests.get(url)
#print("Apple" in resp.text)
html = resp.text

#file = open("memo.txt", "w")
#file.write(html)
#file.close()

bs = BeautifulSoup(resp.text, "html5lib")
#sel ="#rso > div:nth-child(1) > div > div > div > div.yuRUbf > a > h3"
#sel = "#main > div.uEierd > div > div:nth-child(1) > a > div.MUxGbd.v0nnCb.aLF0Z"
sel = "#main > div div div a div"
result = bs.select(sel)

print(result[0].text)

