from kiwoom import *
from selenium import webdriver
import pickle
import time

kiwoom = Kiwoom()
kiwoom.CommConnect()
driver = webdriver.Chrome('chromedriver.exe')
def get_buz_summary(driver, ticker):
    try:
        url = f"http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=&NewMenuID=11&stkGb=701"
        driver.get(url)
    ##driver.switch_to.window(driver.window_handles[-1]) 가장 최근 팝업창으로 창 전환
        sel = "#bizSummaryHeader"
        ui = driver.find_element_by_css_selector(sel)
        return ui.text
    except Exception as error:
        print(error)
        pass

f = open("data.db", "rb")   ##얘는 읽고 주문 넣으면 되니까  r : 리드모드로 가져와
tickers = pickle.load(f)   ## 아까 list로 저장했으니 pickle은 list로 읽어온다
f.close()

file = open("out.txt", "w")

for ticker in tickers:
    name = kiwoom.GetMasterCodeName(ticker)
    summary = get_buz_summary(driver, ticker)
    file.write(f"{name}, {summary}" + "\n")
    time.sleep(1)

file.close()