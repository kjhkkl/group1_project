from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd

def get_chrome_driver():
    chrome_options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    return driver

driver = get_chrome_driver()
url = "https://www.starbucks.co.kr/store/store_map.do?disp=locale"
driver.get(url)
time.sleep(3)

driver.find_element_by_xpath('//*[@id="container"]/div/form/fieldset/div/section/article[1]/article/article[2]/div[1]/div[2]/ul/li[1]/a').click()
time.sleep(3)

driver.find_element_by_xpath('//*[@id="mCSB_2_container"]/ul/li[1]/a').click()
time.sleep(3)

html = driver.page_source
soup = BeautifulSoup(html,"html.parser")

all_store = soup.select("li.quickResultLstCon")
data = []
for i in all_store:
    name = i("strong")[0].text.strip()
    lat = i["data-lat"]
    lng = i["data-long"]
    address = str(i.select("p.result_details")[0]).split('<br/>')[0].split('>')[1]

    data.append([name, lat, lng, address])

columns = ["매장명", "위도", "경도", "주소"]
df = pd.DataFrame(data, columns= columns)
df.to_csv("starbucks_in_seoul.csv", index = False, encoding='utf-8-sig')