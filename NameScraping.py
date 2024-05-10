import csv
import requests
from bs4 import BeautifulSoup


file_name = "취약점_리스트.csv"
f = open(file_name, "w", encoding="utf-8-sig", newline="") # 파일명, 쓰기모드, utf-8 방식으로, newline에 띄어쓰기 없음
writer = csv.writer(f)

columns_name = ["취약점명"]

# writer.writerow(columns_name)

#웹 서버에 요청하기
i = 1
while (i < 5):
    url = "https://vulncat.fortify.com/ko/weakness?po={}".format(i)
    
    res = requests.get(url)
    res.raise_for_status() #상태값


#soup 객체 만들기
    soup = BeautifulSoup(res.text, "lxml")
    weaknessAll = soup.find('div', attrs={"id": "site-canvas1"}) # site-canvas 영역으로 제한

    weaknessBox = weaknessAll.find_all('div', attrs={"class": "detailcell"})

    weaknessTitle = weaknessAll.find_all('div', attrs={"class": "title"}) # 취약점
    weaknesslang = weaknessAll.find_all('div', attrs={"class": "tab-wrapper"}) # 언어

    for title in weaknessTitle:
        name = title.find('a').text
        print(title.find('a').text)

        data_rows = [name]
        
        writer.writerow(data_rows)
        
    i += 1




