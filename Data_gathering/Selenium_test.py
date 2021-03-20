##먼저 네이버 사전으로 연습
from selenium import webdriver


driver = webdriver.Chrome('chromedriver.exe')
driver.get('https://www.naver.com')

##클릭을 구현해보자
selector = "#NM_FAVORITE > div.group_nav > ul.list_nav.NM_FAVORITE_LIST > li:nth-child(3) > a"
ui = driver.find_element_by_css_selector(selector)
ui.click()

selector = "#stock_items"
ui = driver.find_element_by_css_selector(selector)
ui.send_keys("삼성전자")

selector = "#header > div.snb_area > div > div.sta > form > fieldset > div > button"
ui = driver.find_element_by_css_selector(selector)
ui.click()

driver.find_element_by_link_text('삼성전자').click()
###위 코드는 좀 더 수정할 필요가 있음, 범용적이지 못함

selector = "#_market_sum"
ui = driver.find_element_by_css_selector(selector)
print(ui.text)
###근데 네이버 파이넨스같은경우 url이 종목코드로 구분되니까 더 편하게 할 수 있음


