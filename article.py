try:
    from selenium import webdriver
except:
    os.system('pip3 install selenium')
try:
    import chromedriver_autoinstaller
except:
    os.system('pip3 install chromedriver-autoinstaller')
    import chromedriver_autoinstallers
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인

try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')  
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')  

driver.implicitly_wait(10)
driver.get('https://www.google.com')