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

time.sleep(4.0)

soup = BeautifulSoup(page_source, features='html.parser')

names = soup.find_all('span', class_="nickname")

mainFrame = pd.DataFrame(columns=['Name', 'Kill', 'Death', 'Damage'])

for name in names:
    mainFrame = mainFrame._append({'Name': name.text.strip()}, ignore_index=True)

killDiv = soup.find_all('div', class_='table-cell kills')
for i, player in enumerate(killDiv[1:]):
    mainFrame.loc[i, 'Kill'] = player.find("span").text.strip()


deathDiv = soup.find_all('div', class_='table-cell death')
for i, player in enumerate(deathDiv[1:]):
    mainFrame.loc[i, 'Death'] = player.find("span").text.strip()

nextDiv = soup.find_all('div', class_='table-cell damage')
for i, player in enumerate(nextDiv[1:]):
    mainFrame.loc[i, 'Damage'] = player.find("span").text.strip()


### PERFORMANCE PAGE ###

url2 = 'https://bo3.gg/players?period=last_12_months&tiers=s&tab=performance&sort=open_kills&order=desc'

driver.get(url2)
wait = WebDriverWait(driver, 10)

get_url = driver.current_url

wait.until(EC.url_to_be(url2))
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))

if get_url == url2:

    page_source = driver.page_source

time.sleep(4.0)

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

time.sleep(4.0)

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

### Gernade REVIEW ###

url4 = 'https://bo3.gg/players?period=last_12_months&tiers=s&tab=grenades&sort=flash_assist&order=desc'

driver.get(url4)
wait = WebDriverWait(driver, 10)

get_url = driver.current_url

wait.until(EC.url_to_be(url4))
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))

if get_url == url4:

    page_source = driver.page_source

time.sleep(4.0)

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

### Primary REVIEW ###

url5 = 'https://bo3.gg/players?period=last_12_months&tiers=s&tab=primary_devices&sort=ak47_kills&order=desc'

driver.get(url5)
wait = WebDriverWait(driver, 10)

get_url = driver.current_url

wait.until(EC.url_to_be(url5))
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))

if get_url == url5:

    page_source = driver.page_source

time.sleep(4.0)

soup = BeautifulSoup(page_source, features='html.parser')

names = soup.find_all('span', class_="nickname")

gunFrame = pd.DataFrame(columns=['Name', 'AK47-Kill', 'AK47-DMG', 'AWP-Kill', 'AWP-DMG', 'M4A1-Kill', 'M4A1-DMG'])

for name in names:
    gunFrame = gunFrame._append({'Name': name.text.strip()}, ignore_index=True)

nextDiv = soup.find_all('div', class_='table-cell ak47_kills current-sorting')
for i, player in enumerate(nextDiv[1:]):
    gunFrame.loc[i, 'AK47-Kill'] = player.find("span").text.strip()

nextDiv = soup.find_all('div', class_='table-cell ak47_damage')
for i, player in enumerate(nextDiv[1:]):
    gunFrame.loc[i, 'AK47-DMG'] = player.find("span").text.strip()

nextDiv = soup.find_all('div', class_='table-cell awp_kills')
for i, player in enumerate(nextDiv[1:]):
    gunFrame.loc[i, 'AWP-Kill'] = player.find("span").text.strip()

nextDiv = soup.find_all('div', class_='table-cell awp_damage')
for i, player in enumerate(nextDiv[1:]):
    gunFrame.loc[i, 'AWP-DMG'] = player.find("span").text.strip()

nextDiv = soup.find_all('div', class_='table-cell m4a1_kills')
for i, player in enumerate(nextDiv[1:]):
    gunFrame.loc[i, 'M4A1-Kill'] = player.find("span").text.strip()

nextDiv = soup.find_all('div', class_='table-cell m4a1_damage')
for i, player in enumerate(nextDiv[1:]):
    gunFrame.loc[i, 'M4A1-DMG'] = player.find("span").text.strip()


### Pistol REVIEW ###

url6 = 'https://bo3.gg/players?period=last_12_months&tiers=s&tab=pistols&sort=deagle_kills&order=desc'

driver.get(url6)
wait = WebDriverWait(driver, 10)

get_url = driver.current_url

wait.until(EC.url_to_be(url6))
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))

if get_url == url6:

    page_source = driver.page_source

time.sleep(4.0)

soup = BeautifulSoup(page_source, features='html.parser')

names = soup.find_all('span', class_="nickname")

pisFrame = pd.DataFrame(columns=['Name', 'Deagle-Kill', 'Deagle-DMG', 'Glock-Kill', 'Glock-DMG', 'USP-Kill', 'USP-DMG'])

for name in names:
    pisFrame = pisFrame._append({'Name': name.text.strip()}, ignore_index=True)

nextDiv = soup.find_all('div', class_='table-cell deagle_kills current-sorting')
for i, player in enumerate(nextDiv[1:]):
    pisFrame.loc[i, 'Deagle-Kill'] = player.find("span").text.strip()

nextDiv = soup.find_all('div', class_='table-cell deagle_damage')
for i, player in enumerate(nextDiv[1:]):
    pisFrame.loc[i, 'Deagle-DMG'] = player.find("span").text.strip()

nextDiv = soup.find_all('div', class_='table-cell glock_kills')
for i, player in enumerate(nextDiv[1:]):
    pisFrame.loc[i, 'Glock-Kill'] = player.find("span").text.strip()

nextDiv = soup.find_all('div', class_='table-cell glock_damage')
for i, player in enumerate(nextDiv[1:]):
    pisFrame.loc[i, 'Glock-DMG'] = player.find("span").text.strip()

nextDiv = soup.find_all('div', class_='table-cell usp_kills')
for i, player in enumerate(nextDiv[1:]):
    pisFrame.loc[i, 'USP-Kill'] = player.find("span").text.strip()

nextDiv = soup.find_all('div', class_='table-cell usp_damage')
for i, player in enumerate(nextDiv[1:]):
    pisFrame.loc[i, 'USP-DMG'] = player.find("span").text.strip()

### Economy Costs REVIEW ###

url7 = 'https://bo3.gg/players?period=last_12_months&tiers=s&tab=economy&sort=kill_cost&order=desc'

driver.get(url7)
wait = WebDriverWait(driver, 10)

get_url = driver.current_url

wait.until(EC.url_to_be(url7))
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))

if get_url == url7:

    page_source = driver.page_source

time.sleep(4.0)

soup = BeautifulSoup(page_source, features='html.parser')

names = soup.find_all('span', class_="nickname")

ecoFrame = pd.DataFrame(columns=['Name', 'Kill-Cost', 'DMG-Cost', 'Saved-Avg'])

for name in names:
    ecoFrame = ecoFrame._append({'Name': name.text.strip()}, ignore_index=True)

nextDiv = soup.find_all('div', class_='table-cell kill_cost current-sorting')
for i, player in enumerate(nextDiv[1:]):
    ecoFrame.loc[i, 'Kill-Cost'] = player.find("span").text.strip()

nextDiv = soup.find_all('div', class_='table-cell dmg_cost')
for i, player in enumerate(nextDiv[1:]):
    ecoFrame.loc[i, 'DMG-Cost'] = player.find("span").text.strip()

nextDiv = soup.find_all('div', class_='table-cell saved')
for i, player in enumerate(nextDiv[1:]):
    ecoFrame.loc[i, 'Saved-Avg'] = player.find("span").text.strip()

### Kill REVIEW ###

url8 = 'https://bo3.gg/players?period=last_12_months&tiers=s&tab=multikills&sort=multikills_vs_5&order=desc'

driver.get(url8)
wait = WebDriverWait(driver, 10)

get_url = driver.current_url

wait.until(EC.url_to_be(url8))
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))

if get_url == url8:

    page_source = driver.page_source

time.sleep(4.0)

soup = BeautifulSoup(page_source, features='html.parser')

names = soup.find_all('span', class_="nickname")

killFrame = pd.DataFrame(columns=['Name', 'ACE', '4Kill', '3Kill', '2Kill'])

for name in names:
    killFrame = killFrame._append({'Name': name.text.strip()}, ignore_index=True)

nextDiv = soup.find_all('div', class_='table-cell multikills_vs_5 current-sorting')
for i, player in enumerate(nextDiv[1:]):
    killFrame.loc[i, 'ACE'] = player.find("span").text.strip()

nextDiv = soup.find_all('div', class_='table-cell multikills_vs_4')
for i, player in enumerate(nextDiv[1:]):
    killFrame.loc[i, '4Kill'] = player.find("span").text.strip()

nextDiv = soup.find_all('div', class_='table-cell multikills_vs_3')
for i, player in enumerate(nextDiv[1:]):
    killFrame.loc[i, '3Kill'] = player.find("span").text.strip()

nextDiv = soup.find_all('div', class_='table-cell multikills_vs_2')
for i, player in enumerate(nextDiv[1:]):
    killFrame.loc[i, '2Kill'] = player.find("span").text.strip()

### Economy Costs REVIEW ###

url8 = 'https://bo3.gg/players?period=last_12_months&tiers=s&tab=clutches&sort=clutches_vs_5&order=desc'

driver.get(url8)
wait = WebDriverWait(driver, 10)

get_url = driver.current_url

wait.until(EC.url_to_be(url8))
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))

if get_url == url8:

    page_source = driver.page_source

time.sleep(4.0)

soup = BeautifulSoup(page_source, features='html.parser')

names = soup.find_all('span', class_="nickname")

cluFrame = pd.DataFrame(columns=['Name', '5v1', '4v1', '3v1', '2v1', '1v1'])

for name in names:
    cluFrame = cluFrame._append({'Name': name.text.strip()}, ignore_index=True)

nextDiv = soup.find_all('div', class_='table-cell clutches_vs_5 current-sorting')
for i, player in enumerate(nextDiv[1:]):
    cluFrame.loc[i, '5v1'] = player.find("span").text.strip()

nextDiv = soup.find_all('div', class_='table-cell clutches_vs_4')
for i, player in enumerate(nextDiv[1:]):
    cluFrame.loc[i, '4v1'] = player.find("span").text.strip()

nextDiv = soup.find_all('div', class_='table-cell clutches_vs_3')
for i, player in enumerate(nextDiv[1:]):
    cluFrame.loc[i, '3v1'] = player.find("span").text.strip()

nextDiv = soup.find_all('div', class_='table-cell clutches_vs_2')
for i, player in enumerate(nextDiv[1:]):
    cluFrame.loc[i, '2v1'] = player.find("span").text.strip()

    nextDiv = soup.find_all('div', class_='table-cell clutches_vs_1')
for i, player in enumerate(nextDiv[1:]):
    cluFrame.loc[i, '1v1'] = player.find("span").text.strip()

### Merging and Output ###

dfs = [mainFrame, perFrame, killFrame, aimFrame, cluFrame, gerFrame, gunFrame, pisFrame]

merged_df = pd.concat([df.set_index('Name') for df in dfs], axis=1, join='outer').reset_index()

merged_df.to_csv('cs_stier_data.csv', index=False)

driver.quit()

