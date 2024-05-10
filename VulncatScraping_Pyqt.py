import sys
import requests
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from bs4 import BeautifulSoup
from datetime import datetime


form_class = uic.loadUiType("vulncat.ui")[0]

class Main(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.btn1.clicked.connect(self.Btn1Function)
        self.btn2.clicked.connect(QCoreApplication.instance().quit)
        
        
        
    #============================================================
        
    def Btn1Function(self):
        
        self.label.setText("데이터 불러오는 중...")
        
        #웹 서버에 요청하기
        weakness = []
        page = 1
        while (page < 4):
            url = "https://vulncat.fortify.com/ko/weakness?po={}".format(page)
            
            res = requests.get(url)
            res.raise_for_status() #상태값


        #soup 객체 만들기
            soup = BeautifulSoup(res.text, "lxml")
            weaknessAll = soup.find("div", attrs={"id": "site-canvas1"}) # site-canvas 영역으로 제한

            weaknessBox = weaknessAll.find_all("div", attrs={"class": "detailcell"}) # 각 취약점 박스
            

            for info in weaknessBox: # 취약점 박스 안의 정보들을 가져오자.
                name = info.find("div", attrs={"class": "title"}) # 
                languages = info.find_all("li", attrs={"role": "presentation"}) # 언어
                contents = info.find_all("div", attrs={"class": "t"}) # 내용(abstract/explanation/reference)
                
                content = []
                for li in range(0, len(contents), 3):
                    content.append(contents[li:li+3])
                
                print(name.text)
                print(len(languages))
                print(len(contents))

                i = 0
                # lanNum = languages[i]
                
                for lang in languages:
                    try: # 내용 부분이 비어있을 경우 리스트 out of range에러가 발생하기 때문에 예외처리
                        weakness.append([name.text, languages[i].text, content[i][0].text, content[i][1].text, content[i][2].text])
                    except IndexError:
                        print("내용이 없습니다.")
                        pass
                    i += 1
                    
            page += 1
                    
            df = pd.DataFrame(weakness, columns=['취약점명', '언어', '요약', '상세', '참조'])
            today = datetime.today().strftime("%Y%m%d")
            
            with pd.ExcelWriter('Vulncat_{}.xlsx'.format(today), engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='취약점리스트')
                
                sheet = writer.sheets['취약점리스트']
                
                sheet.column_dimensions['A'].width = 50
                sheet.column_dimensions['B'].width = 25
                sheet.column_dimensions['C'].width = 50 
                sheet.column_dimensions['D'].width = 50 
                sheet.column_dimensions['E'].width = 50 
            
        self.label.clear()
        self.label.setText("데이터 스크래핑 완료")
            
        
    def Btn2Function(self):
        print("종료")
        
        
        
    #============================================================
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    app.exec_()
        
        
        
        
#======================================================================================



        
    



