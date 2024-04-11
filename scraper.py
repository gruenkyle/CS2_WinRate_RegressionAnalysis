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

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get(url)
wait = WebDriverWait(driver, 10)

get_url = driver.current_url

wait.until(EC.url_to_be(url))
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))

if get_url == url:

    page_source = driver.page_source

button = WebDriverWait(driver, 10).until(
     EC.element_to_be_clickable((By.CSS_SELECTOR, "button.c-button.c-button--full-width"))
)

button.click()

time.sleep(2.0)

soup = BeautifulSoup(page_source, features='html.parser')

names = soup.find_all('span', class_="nickname")

mainFrame = pd.DataFrame(columns=['Name', 'Kill', 'Death'])

for name in names:
    mainFrame = mainFrame._append({'Name': name.text.strip()}, ignore_index=True)

killDiv = soup.find_all('div', class_='table-cell kills')
for i, player in enumerate(killDiv[1:]):
    mainFrame.loc[i, 'Kill'] = player.find("span").text.strip()


deathDiv = soup.find_all('div', class_='table-cell death')
for i, player in enumerate(deathDiv[1:]):
    mainFrame.loc[i, 'Death'] = player.find("span").text.strip()


### PERFORMANCE PAGE ###

url2 = 'https://bo3.gg/players?period=last_12_months&tiers=s&tab=performance&sort=open_kills&order=desc'

driver.get(url2)
wait = WebDriverWait(driver, 10)

get_url = driver.current_url

wait.until(EC.url_to_be(url2))
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))

if get_url == url2:

    page_source = driver.page_source

time.sleep(2.0)

soup = BeautifulSoup(page_source, features='html.parser')

names = soup.find_all('span', class_="nickname")

perFrame = pd.DataFrame(columns=['Name', 'O_Kill', 'O_Death', 'Trade', 'Assist'])

for name in names:
    perFrame = perFrame._append({'Name': name.text.strip()}, ignore_index=True)

okDiv = soup.find_all('div', class_='table-cell open_kills current-sorting')
for i, player in enumerate(okDiv[1:]):
    perFrame.loc[i, 'O_Kill'] = player.find("span").text.strip()

odDiv = soup.find_all('div', class_='table-cell open_death')
for i, player in enumerate(odDiv[1:]):
    perFrame.loc[i, 'O_Death'] = player.find("span").text.strip()

tradeDiv = soup.find_all('div', class_='table-cell trades')
for i, player in enumerate(tradeDiv[1:]):
    perFrame.loc[i, 'Trade'] = player.find("span").text.strip()

assistDiv = soup.find_all('div', class_='table-cell assists')
for i, player in enumerate(assistDiv[1:]):
    perFrame.loc[i, 'Assist'] = player.find("span").text.strip()

### AIM REVIEW ###

url3 = 'https://bo3.gg/players?period=last_12_months&tiers=s&tab=aim&sort=headshots&order=desc'

driver.get(url3)
wait = WebDriverWait(driver, 10)

get_url = driver.current_url

wait.until(EC.url_to_be(url3))
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))

if get_url == url3:

    page_source = driver.page_source

time.sleep(2.0)

soup = BeautifulSoup(page_source, features='html.parser')

names = soup.find_all('span', class_="nickname")

aimFrame = pd.DataFrame(columns=['Name', 'Headshot', 'HeadshotPer', 'Shot', 'ShotPer'])

for name in names:
    aimFrame = aimFrame._append({'Name': name.text.strip()}, ignore_index=True)

headDiv = soup.find_all('div', class_='table-cell headshots current-sorting')
for i, player in enumerate(headDiv[1:]):
    aimFrame.loc[i, 'Headshot'] = player.find("span").text.strip()

headPerDiv = soup.find_all('div', class_='table-cell headshot_kills_accuracy')
for i, player in enumerate(headPerDiv[1:]):
    aimFrame.loc[i, 'HeadshotPer'] = player.find("p").text.strip()

shotDiv = soup.find_all('div', class_='table-cell shots')
for i, player in enumerate(shotDiv[1:]):
    aimFrame.loc[i, 'Shot'] = player.find("span").text.strip()

accDiv = soup.find_all('div', class_='table-cell accuracy')
for i, player in enumerate(accDiv[1:]):
    aimFrame.loc[i, 'ShotPer'] = player.find("p").text.strip()

### AIM REVIEW ###

url4 = 'https://bo3.gg/players?period=last_12_months&tiers=s&tab=grenades&sort=flash_assist&order=desc'

driver.get(url4)
wait = WebDriverWait(driver, 10)

get_url = driver.current_url

wait.until(EC.url_to_be(url4))
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))

if get_url == url4:

    page_source = driver.page_source

time.sleep(2.0)

soup = BeautifulSoup(page_source, features='html.parser')

names = soup.find_all('span', class_="nickname")

gerFrame = pd.DataFrame(columns=['Name', 'FlashAssist', 'FlashBlind', 'FlashDuration', 'MolDMG', 'HeDMG'])

for name in names:
    gerFrame = gerFrame._append({'Name': name.text.strip()}, ignore_index=True)

nextDiv = soup.find_all('div', class_='table-cell flash_assist current-sorting')
for i, player in enumerate(nextDiv[1:]):
    gerFrame.loc[i, 'FlashAssist'] = player.find("span").text.strip()

nextDiv = soup.find_all('div', class_='table-cell flash_blinded')
for i, player in enumerate(nextDiv[1:]):
    gerFrame.loc[i, 'FlashBlind'] = player.find("span").text.strip()

nextDiv = soup.find_all('div', class_='table-cell flash_duration')
for i, player in enumerate(nextDiv[1:]):
    gerFrame.loc[i, 'FlashDuration'] = player.find("span").text.strip()

nextDiv = soup.find_all('div', class_='table-cell molotov_damage')
for i, player in enumerate(nextDiv[1:]):
    gerFrame.loc[i, 'MolDMG'] = player.find("span").text.strip()

nextDiv = soup.find_all('div', class_='table-cell he_damage')
for i, player in enumerate(nextDiv[1:]):
    gerFrame.loc[i, 'HeDMG'] = player.find("span").text.strip()

print(gerFrame)

driver.quit()

