import os
import datetime
try:
    from selenium import webdriver
except:
    os.system('pip3 install selenium')
    from selenium import webdriver
from selenium.webdriver.common.by import By
try:
    import chromedriver_autoinstaller
except:
    os.system('pip3 install chromedriver-autoinstaller')
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
        if company.text == '기업':
            break
        company_list.append(company.text)
    return company_list

def get_articles():
    for i in range(400):
        url = f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EB%A9%94%ED%83%80%EB%B2%84%EC%8A%A4%20%EC%A7%84%EC%B6%9C&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=28&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start={i}1'
        driver.get(url)
        articles = driver.find_elements(By.CLASS_NAME, 'bx')
    return articles

def get_article_info(article):
    today = datetime.date.today()
    article_info = dict()
    article_info['title'] = article.find_element(By.CLASS_NAME, 'news-tit').text
    article_info['date'] = article.find_elements(By.CLASS_NAME, 'info')[-1].text
    if article_info['date'][-1] == '전':
        if article_info['date'][-3] == '일':
            date = today - datetime.timedelta(days=int(article_info['date'][:-3]))
            article_info['date'] = datetime.date.strftime(date, '%Y.%m.%d')
        elif article_info['date'][-3] == '주':
            date = today - datetime.timedelta(weeks=int(article_info['date'][:-3]))
            article_info['date'] = datetime.date.strftime(date, '%Y.%m.%d')
    return article_info

def make_article_data(article):
    article_info = get_article_info(article)
    for article in get_articles():
        for company in get_company_list():
            pass
            

if __name__ == '__main__':
    get_articles()