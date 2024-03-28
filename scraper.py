from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import pandas as pd
import numpy as np

import time

from webdriver_manager.chrome import ChromeDriverManager

url = "https://bo3.gg/players?period=last_12_months&tiers=s&tab=main&sort=rating&order=desc"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get(url)
wait = WebDriverWait(driver, 10)

get_url = driver.current_url

wait.until(EC.url_to_be(url))
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))

if get_url == url:

    page_source = driver.page_source

driver.find_element(By.CLASS_NAME, 'c-button c-button--full-width').click()

driver.execute_script("window.scrollTo(0, 2400)")

SCROLL_PAUSE_TIME = 3.5
time.sleep(SCROLL_PAUSE_TIME)


soup = BeautifulSoup(page_source, features='html.parser')

time.sleep(SCROLL_PAUSE_TIME)

names = soup.find_all('span', class_="nickname")

mainFrame = pd.DataFrame(columns=['Name'])

for name in names:
    mainFrame = mainFrame._append({'Name': name.text.strip()}, ignore_index=True)

driver.quit()

print(mainFrame.shape)