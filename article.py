import os
import datetime
os.system('pip3 install -r requirements.txt')
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')  
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')  

driver.implicitly_wait(1) # 요 위에 까지는 코드를 실행하기 위한 준비

def get_company_list(): # 한국거래소에 등록되어있는 주식 종목의 목록을 리스트화
    stock_code = pd.read_csv('stock_code.csv', encoding='cp949')
    company_list = list(stock_code['종목명'])
    return company_list

def write_raw_data(): # 네이버에서 "메타버스 진출" 검색어로 검색하여 기사의 제목과 발행 일자를 텍스트 파일로 저장
    with open('article_raw_data.txt', 'w', encoding='utf-8') as f: # 텍스트 파일 열기
        f.truncate()
        f.seek(0)
        for i in range(400): 
            url = f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EB%A9%94%ED%83%80%EB%B2%84%EC%8A%A4%20%EC%A7%84%EC%B6%9C&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=28&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start={i}1'
            driver.get(url) # 네이버 기사 창 열기
            titles = [title.text for title in driver.find_elements(By.CLASS_NAME, 'news_tit')] # 기사 제목 따오기
            dates = [date.text for date in driver.find_elements(By.CLASS_NAME, 'info') if date.text[-1] == '전' or date.text[0:3] == '202'] # 발행 일자 따오기
            for title, date in zip(titles, dates):
                f.write(f'{title}\t{date}\n') # 기사 제목과 발행 일자를 그대로 텍스트 파일에 쓰기

def write_data(): # 데이터 정리
    today = datetime.date.today()
    data = list()
    df = pd.read_csv('stock_code.csv', encoding='cp949')
    with open('article_raw_data.txt', 'r', encoding='utf-8') as f: # 위에서 써둔 데이터 읽기
        with open('article_data.txt', 'w', encoding='utf-8') as f2: # 정리된 데이터를 쓸 텍스트 파일 열기
            f2.truncate()
            f2.seek(0)
            for line in f:
                line = line.strip()
                title, date = line.split('\t')
                for company in get_company_list():
                    if company in title: # 기사 제목에 기업명이 있는지 검사
                        if date[-1] == '전': # 발행 일자가 '~전'이라 되어있으면 날짜로 고치기
                            if date[-3] == '일':
                                date = today - datetime.timedelta(days=int(date[:-3]))
                                date = datetime.date.strftime(date, '%Y.%m.%d.')
                            elif date[-3] == '주':
                                date = today - datetime.timedelta(weeks=int(date[:-3]))
                                date = datetime.date.strftime(date, '%Y.%m.%d.')
                        data.append((company, date))
            data = list(set(data)) # 중복제거
            for company, date in data:
                code = df.loc[df['종목명'] == company, '종목코드'].values[0] # 기업명에 맞는 종목 코드를 찾기
                if len(str(code)) < 6:
                    code = '0'*(6-len(str(code))) + str(code)
                f2.write(f'{company}\t{date}\t{code}\n') # 텍스트 파일에 쓰기

write_data()
