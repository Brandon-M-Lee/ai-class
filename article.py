import os
import datetime
os.system('pip3 install -r requirements.txt')
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인

try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')  
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')  

driver.implicitly_wait(10)

def get_company_list():
    company_list = list()
    driver.get('https://ko.wikipedia.org/wiki/%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EA%B8%B0%EC%97%85_%EB%AA%A9%EB%A1%9D')
    companys = driver.find_elements(By.TAG_NAME, 'li')
    for company in companys:
        if not company.text:
            continue
        company_list.append(company.text)
    return company_list[29:-15]

def get_articles():
    article_titles = list()
    article_infos = list()
    article_dates = list()
    for i in range(400):
        url = f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EB%A9%94%ED%83%80%EB%B2%84%EC%8A%A4%20%EC%A7%84%EC%B6%9C&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=28&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start={i}1'
        driver.get(url)
        for article_title in driver.find_elements(By.CLASS_NAME, 'new-tit'):
            article_titles.append(article_title)
        for article_info in driver.find_elements(By.CLASS_NAME, 'info'):
            article_infos.append(article_info)
    for article_info in article_infos:
        try:
            if article_info.text[-1] == '전' or article_info.text[0:4] == '2022':
                article_dates.append(article_info.text)
        except:
            pass
    path = 'article_data_raw.txt'
    with open(path, 'w', encoding='cp949') as f:
        for i in range(min(len(article_titles), len(article_dates))):
            f.write(f'{article_titles[i].text}\t{article_dates[i]}\n')
    return article_titles, article_dates

def get_article_infos():
    article_infos = list()
    article_titles, article_dates = get_articles()
    for i in range(min(len(article_titles), len(article_dates))):
        article_info = dict()
        article_info['title'] = article_titles[i].text
        article_info['date'] = article_dates[i].text
        today = datetime.date.today()
        if article_info['date'][-1] == '전':
            if article_info['date'][-3] == '일':
                date = today - datetime.timedelta(days=int(article_info['date'][:-3]))
                article_info['date'] = datetime.date.strftime(date, '%Y.%m.%d')
            elif article_info['date'][-3] == '주':
                date = today - datetime.timedelta(weeks=int(article_info['date'][:-3]))
                article_info['date'] = datetime.date.strftime(date, '%Y.%m.%d')
        article_infos.append(article_info)
    return article_infos

def make_article_data():
    path = './article_data.txt'
    with open(path, 'w', encoding='cp949') as f:
        for article_info in get_article_infos():
            for company in get_company_list():
                if company in article_info['title']:
                    f.write(f'{company}\t{article_info["date"]}\n')

if __name__ == '__main__':
    make_article_data()