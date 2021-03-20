from kiwoom import *
import pickle

class PyMon:
    def __init__(self):
        #키움클래스 객체생성
        self.kiwoom = Kiwoom()  ##바인딩까지
        self.kiwoom.CommConnect() ##로그인 호출
        self.kiwoom.GetConditionLoad()  ##조건식 호출

    def run(self):    ### 조건식에 해당하는 종목 리스트를 가져와서 저장하는 것 구현
        self.kiwoom.SendCondition("0101","02_Try", "001", 0)  ##마지막 0은 일반조회
        codes = self.kiwoom.condition_codes
        ####파일로 가져오기

        f = open("data.db", "wb")   ###파일형시 db로 저장, w는 쓰기모드 , b는 바이너리파일이라는 의미
        pickle.dump(codes, f) ### 말그대로 덤프해주기 위해 pickle import, 파일을 쓰는 동작이 반복문으로 구성하는데
                                ### 그렇게 하면 다시 읽오는 과정도 파이썬 리스트로 재구성 해야하지만
        ###pickle로 dump시키면 그대로 넣고 그대로 가져옴  ##초보자일때 좋음
        f.close()


if __name__ == "__main__":  ###실행되는 코드
    pymon = PyMon()   ##객체 생성
    pymon.run()     #매소드 호출해서 실행시키는