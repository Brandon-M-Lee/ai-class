import os
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
start = 1
url = f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EB%A9%94%ED%83%80%EB%B2%84%EC%8A%A4&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=247&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start={start}'

def get_article():
    article_links = list()
    driver.get(url)
    articles = driver.find_elements(By.CLASS_NAME, 'news-tit')
    for article in articles:
        title = article.text
        if '참여' in title or '구축' in title or '사업' in title or