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

driver.implicitly_wait(10)

def get_company_list():
    path = 'stock_code.csv'
    stock_code = pd.read_csv(path, encoding='cp949')
    company_list = list(stock_code['종목명'])
    return company_list

def write_raw_data():
    path = 'article_raw_data.txt'
    with open(path, 'w', encoding='utf-8') as f:
        f.truncate()
        f.seek(0)
        for i in range(400):
            url = f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EB%A9%94%ED%83%80%EB%B2%84%EC%8A%A4%20%EC%A7%84%EC%B6%9C&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=28&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start={i}1'
            driver.get(url)
            titles = [title.text for title in driver.find_elements(By.CLASS_NAME, 'news_tit')]
            dates = [date.text for date in driver.find_elements(By.CLASS_NAME, 'info') if date.text[-1] == '전' or date.text[0:3] == '202']
            for title, date in zip(titles, dates):
                f.write(f'{title}\t{date}\n')

def write_data():
    today = datetime.date.today()
    raw_path = 'article_raw_data.txt'
    path = 'article_data.txt'
    data = list()
    with open(raw_path, 'r', encoding='utf-8') as f:
        with open(path, 'w', encoding='utf-8') as f2:
            f2.truncate()
            f2.seek(0)
            for line in f:
                line = line.strip()
                title, date = line.split('\t')
                for company in get_company_list():
                    if company in title:
                        if date[-1] == '전':
                            if date[-3] == '일':
                                date = today - datetime.timedelta(days=int(date[:-3]))
                                date = datetime.date.strftime(date, '%Y.%m.%d.')
                            elif date[-3] == '주':
                                date = today - datetime.timedelta(weeks=int(date[:-3]))
                                date = datetime.date.strftime(date, '%Y.%m.%d.')
                        data.append((company, date))
            data = list(set(data))
            for company, date in data:
                f2.write(f'{company}\t{date}\n')

write_data()