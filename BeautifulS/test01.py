import requests
from bs4 import BeautifulSoup

url = "https://www.naver.com/"
resp = requests.get(url)


bs = BeautifulSoup(resp.text, "html5lib")
#print(type(bs))
sel = "#NM_FAVORITE > div.group_nav > ul.list_nav.NM_FAVORITE_LIST > li > a"
#"#NM_FAVORITE > div.group_nav > ul.list_nav.NM_FAVORITE_LIST > li > a"
result = bs.select(sel)

for item in result:
    print(item.text)

## 여기서 무엇을 파싱할 것 인가
## 퀄리티?- html5lib 속도?-html.paser