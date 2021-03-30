import requests
from bs4 import BeautifulSoup

url = "https://finance.naver.com/"
resp = requests.get(url)



soup = BeautifulSoup(url, "html5lib")


print( resp.text)
print( "유럽증시" in resp.text)
## 여기서 무엇을 파싱할 것 인가
## 퀄리티?- html5lib 속도?-html.paser
