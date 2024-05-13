import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


print("VulncatScraper를 실행합니다.")
print("데이터를 불러오는 중")

#웹 서버에 요청하기
weakness = []
page = 1
while (page < 2):
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
    print(page, "페이지 스크래핑 완료")
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

