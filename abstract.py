import requests
from bs4 import BeautifulSoup
import openpyxl


wb = openpyxl.Workbook()

sheet = wb.active

sheet.column_dimensions["A"].width = 50
sheet.column_dimensions["B"].width = 40
sheet.column_dimensions["C"].width = 150


sheet.append(["취약점명", "언어", "설명"]) # 취약점명, 언어, abstract




#웹 서버에 요청하기
page = 1
while (page < 2):
    url = "https://vulncat.fortify.com/ko/weakness?po={}".format(page)
    
    res = requests.get(url)
    res.raise_for_status() #상태값


#soup 객체 만들기
    soup = BeautifulSoup(res.text, "lxml")
    weaknessAll = soup.find("div", attrs={"id": "site-canvas1"}) # site-canvas 영역으로 제한

    weaknessBox = weaknessAll.find_all("div", attrs={"class": "detailcell"}) # 각 취약점 박스
    
    weakness = []

    for info in weaknessBox:
        name = info.find("div", attrs={"class": "title"})
        languages = info.find_all("li", attrs={"role": "presentation"}) # 언어
        contents = info.find_all("div", attrs={"class": "t"}) # 내용(abstract만) - find로 찾음
        
        print(name.text)
        data_row = [name.text] # row에 이름 추가
        
        for lang in languages:
            print(lang.text)
            data_row.append(lang.text)
            
            for content in contents:
                print(content.text)
                data_row.append(lang.text)
            
            
        
        # langList = ', '.join([lang.text for lang in languages]) # for문 돌려서 나온 lang들을 ,로 구분하여 리스트로 합침
        # print(langList)
        # data_row.append(langList) # row에 언어 추가
        
        # print(content.text)
        # data_row.append(content.text) # row에 abstract 추가
        
        sheet.append(data_row) # 위 내용들을 sheet에 append
        
    page += 1
    
    wb.save("취약점_리스트.xlsx")




