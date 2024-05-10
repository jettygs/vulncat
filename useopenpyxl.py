import csv
import requests
from bs4 import BeautifulSoup
import openpyxl


wb = openpyxl.Workbook()

sheet = wb.active

sheet.column_dimensions['A'].width = 50
sheet.column_dimensions['B'].width = 50
sheet.column_dimensions['C'].width = 50
sheet.column_dimensions['D'].width = 50


sheet.append(["취약점명", "내용1", "내용2", "내용3"])


#웹 서버에 요청하기
i = 1
while (i < 2):
    url = "https://vulncat.fortify.com/ko/weakness?po={}".format(i)
    
    res = requests.get(url)
    res.raise_for_status() #상태값


#soup 객체 만들기
    soup = BeautifulSoup(res.text, "lxml")
    weaknessAll = soup.find('div', attrs={"id": "site-canvas1"}) # site-canvas 영역으로 제한

    weaknessBox = weaknessAll.find_all('div', attrs={"class": "detailcell"})


    # print(weaknessBody) 


    for info in weaknessBox:
        name = info.find('div', attrs={"class": "title"})
        contents = info.find_all('div', attrs={"class": "t"}) # 내용
        
        print("contets의 길이:", len(contents))
        print(name.text)
        
        data_row = [name.text] # row에 이름 추가
        
        for content in contents:
            print(content.text)

            data_row.append(content.text) # row에 내용1,2,3 추가
        
        sheet.append(data_row) # 이름과 내용을 엑셀에 write
        
    i += 1
    
    wb.save("취약점_리스트.xlsx")




