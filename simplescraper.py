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

URLS = ['https://bo3.gg/players?period=last_12_months&tiers=a&tab=main&sort=rating&order=desc',
        'https://bo3.gg/players?period=last_12_months&tiers=a&tab=main&sort=rating&order=desc&page=2',
        'https://bo3.gg/players?period=last_12_months&tiers=a&tab=performance&sort=open_kills&order=desc',
        'https://bo3.gg/players?period=last_12_months&tiers=a&tab=performance&sort=open_kills&order=desc&page=2',
        'https://bo3.gg/players?period=last_12_months&tiers=a&tab=aim&sort=headshots&order=desc',
        'https://bo3.gg/players?period=last_12_months&tiers=a&tab=aim&sort=headshots&order=desc&page=2',
        'https://bo3.gg/players?period=last_12_months&tiers=a&tab=grenades&sort=flash_assist&order=desc',
        'https://bo3.gg/players?period=last_12_months&tiers=a&tab=grenades&sort=flash_assist&order=desc&page=2',
        'https://bo3.gg/players?period=last_12_months&tiers=a&tab=primary_devices&sort=ak47_kills&order=desc',
        'https://bo3.gg/players?period=last_12_months&tiers=a&tab=primary_devices&sort=ak47_kills&order=desc&page=2',
        'https://bo3.gg/players?period=last_12_months&tiers=a&tab=pistols&sort=deagle_kills&order=desc',
        'https://bo3.gg/players?period=last_12_months&tiers=a&tab=pistols&sort=deagle_kills&order=desc&page=2',
        'https://bo3.gg/players?period=last_12_months&tiers=a&tab=economy&sort=kill_cost&order=desc',
        'https://bo3.gg/players?period=last_12_months&tiers=a&tab=economy&sort=kill_cost&order=desc&page=2',
        'https://bo3.gg/players?period=last_12_months&tiers=a&tab=multikills&sort=multikills_vs_5&order=desc',
        'https://bo3.gg/players?period=last_12_months&tiers=a&tab=multikills&sort=multikills_vs_5&order=desc&page=2',
        'https://bo3.gg/players?period=last_12_months&tiers=a&tab=clutches&sort=clutches_vs_5&order=desc',
        'https://bo3.gg/players?period=last_12_months&tiers=a&tab=clutches&sort=clutches_vs_5&order=desc&page=2']

links = pd.DataFrame({'URL': URLS})

RANKS = ['s', 'a', 'b']

MAINCLASS = ['table-cell rating current-sorting' 'table-cell kills', 'table-cell death', 'table-cell damage']

PERCLASS = ['table-cell open_kills current-sorting', 'table-cell open_death', 
            'table-cell trades', 'table-cell assists']

AIMCLASS = ['table-cell headshots current-sorting', 'table-cell headshot_kills_accuracy',
            'table-cell shots', 'table-cell accuracy']

GERCLASS = ['table-cell flash_assist current-sorting', 'table-cell flash_blinded',
            'table-cell flash_duration', 'table-cell molotov_damage', 'table-cell he_damage']

GUNCLASS = ['table-cell ak47_kills current-sorting', 'table-cell ak47_damage', 'table-cell awp_kills', 
            'table-cell awp_damage', 'table-cell m4a1_kills', 'table-cell m4a1_damage']

PISCLASS = ['table-cell deagle_kills current-sorting', 'table-cell deagle_damage', 'table-cell glock_kills',
            'table-cell glock_damage', 'table-cell usp_kills', 'table-cell usp_damage']

ECOCLASS = ['table-cell kill_cost current-sorting', 'table-cell dmg_cost', 'table-cell saved']

KILCLASS = ['table-cell multikills_vs_5 current-sorting', 'table-cell multikills_vs_4', 
            'table-cell multikills_vs_3', 'table-cell multikills_vs_2']

CLUCLASS = ['table-cell clutches_vs_5 current-sorting', 'table-cell clutches_vs_4', 
            'table-cell clutches_vs_3', 'table-cell clutches_vs_2',
            'table-cell clutches_vs_1']

######

mainFrame = pd.DataFrame(columns=['Name', 'Score', 'Kill', 'Death', 'Damage', 'PlayCount'])
mainFrame2 = pd.DataFrame(columns=['Name', 'Score', 'Kill', 'Death', 'Damage', 'PlayCount'])

perFrame = pd.DataFrame(columns=['Name', 'O_Kill', 'O_Death', 'Trade', 'Assist'])
perFrame2 = pd.DataFrame(columns=['Name', 'O_Kill', 'O_Death', 'Trade', 'Assist'])

aimFrame = pd.DataFrame(columns=['Name', 'Headshot', 'HeadshotPer', 'Shot', 'ShotPer'])
aimFrame2 = pd.DataFrame(columns=['Name', 'Headshot', 'HeadshotPer', 'Shot', 'ShotPer'])

gerFrame = pd.DataFrame(columns=['Name', 'FlashAssist', 'FlashBlind', 'FlashDuration', 'MolDMG', 'HeDMG'])
gerFrame2 = pd.DataFrame(columns=['Name', 'FlashAssist', 'FlashBlind', 'FlashDuration', 'MolDMG', 'HeDMG'])

gunFrame = pd.DataFrame(columns=['Name', 'AK47-Kill', 'AK47-DMG', 'AWP-Kill', 'AWP-DMG', 'M4A1-Kill', 'M4A1-DMG'])
gunFrame2 = pd.DataFrame(columns=['Name', 'AK47-Kill', 'AK47-DMG', 'AWP-Kill', 'AWP-DMG', 'M4A1-Kill', 'M4A1-DMG'])

pisFrame = pd.DataFrame(columns=['Name', 'Deagle-Kill', 'Deagle-DMG', 'Glock-Kill', 'Glock-DMG', 'USP-Kill', 'USP-DMG'])
pisFrame2 = pd.DataFrame(columns=['Name', 'Deagle-Kill', 'Deagle-DMG', 'Glock-Kill', 'Glock-DMG', 'USP-Kill', 'USP-DMG'])

ecoFrame = pd.DataFrame(columns=['Name', 'Kill-Cost', 'DMG-Cost', 'Saved-Avg'])
ecoFrame2 = pd.DataFrame(columns=['Name', 'Kill-Cost', 'DMG-Cost', 'Saved-Avg'])

killFrame = pd.DataFrame(columns=['Name', 'ACE', '4Kill', '3Kill', '2Kill'])
killFrame2 = pd.DataFrame(columns=['Name', 'ACE', '4Kill', '3Kill', '2Kill'])

cluFrame = pd.DataFrame(columns=['Name', '5v1', '4v1', '3v1', '2v1', '1v1'])
cluFrame2 = pd.DataFrame(columns=['Name', '5v1', '4v1', '3v1', '2v1', '1v1'])


######################

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


for j, URL in links['URL'].items(): 
        
        URL = str(URL)

        print("Link " + str(j) + ": " + URL)

        driver.get(URL)
        wait = WebDriverWait(driver, 10)

        get_url = driver.current_url

        if get_url == URL:

                page_source = driver.page_source

        if j == 0:
                button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.c-button.c-button--full-width")))

                button.click()


        wait.until(EC.url_to_be(URL))

        if j == 0: 
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))

                soup = BeautifulSoup(page_source, features='lxml')

                names = soup.find_all('span', class_="nickname")
                
                for name in names:
                        mainFrame = mainFrame._append({'Name': name.text.strip()}, ignore_index=True)
                        
                scoreDiv = soup.find_all('div', class_='table-cell rating current-sorting')
                for i, player in enumerate(scoreDiv[1:]):        
                        mainFrame.loc[i, 'Score'] = player.find("span").text.strip()

                killDiv = soup.find_all('div', class_='table-cell kills')
                for i, player in enumerate(killDiv[1:]):        
                        mainFrame.loc[i, 'Kill'] = player.find("span").text.strip()

                deathDiv = soup.find_all('div', class_='table-cell death')
                for i, player in enumerate(deathDiv[1:]):       
                        mainFrame.loc[i, 'Death'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell damage')
                for i, player in enumerate(nextDiv[1:]):        
                        mainFrame.loc[i, 'Damage'] = player.find("span").text.strip()
                        
                nextDiv = soup.find_all('div', class_='table-cell games_count')
                for i, player in enumerate(nextDiv[1:]):        
                        mainFrame.loc[i, 'PlayCount'] = player.find("p").text.strip()
        
        if j == 1: 
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))

                soup = BeautifulSoup(page_source, features='lxml')

                names = soup.find_all('span', class_="nickname")
                
                for name in names:
                        mainFrame2 = mainFrame2._append({'Name': name.text.strip()}, ignore_index=True)
                        
                scoreDiv = soup.find_all('div', class_='table-cell rating current-sorting')
                for i, player in enumerate(scoreDiv[1:]):        
                        mainFrame2.loc[i, 'Score'] = player.find("span").text.strip()

                killDiv = soup.find_all('div', class_='table-cell kills')
                for i, player in enumerate(killDiv[1:]):        
                        mainFrame2.loc[i, 'Kill'] = player.find("span").text.strip()

                deathDiv = soup.find_all('div', class_='table-cell death')
                for i, player in enumerate(deathDiv[1:]):       
                        mainFrame2.loc[i, 'Death'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell damage')
                for i, player in enumerate(nextDiv[1:]):        
                        mainFrame2.loc[i, 'Damage'] = player.find("span").text.strip()
                        
                nextDiv = soup.find_all('div', class_='table-cell games_count')
                for i, player in enumerate(nextDiv[1:]):        
                        mainFrame2.loc[i, 'PlayCount'] = player.find("p").text.strip()

                mainFrame = mainFrame._append(mainFrame2, ignore_index=True)
                print(mainFrame)

        if j == 2:
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))

                soup = BeautifulSoup(page_source, features='lxml')

                names = soup.find_all('span', class_="nickname")

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

        if j == 3:
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))

                soup = BeautifulSoup(page_source, features='lxml')

                names = soup.find_all('span', class_="nickname")

                for name in names:
                        perFrame2 = perFrame2._append({'Name': name.text.strip()}, ignore_index=True)

                okDiv = soup.find_all('div', class_='table-cell open_kills current-sorting')
                for i, player in enumerate(okDiv[1:]):
                        perFrame2.loc[i, 'O_Kill'] = player.find("span").text.strip()

                odDiv = soup.find_all('div', class_='table-cell open_death')
                for i, player in enumerate(odDiv[1:]):
                        perFrame2.loc[i, 'O_Death'] = player.find("span").text.strip()

                tradeDiv = soup.find_all('div', class_='table-cell trades')
                for i, player in enumerate(tradeDiv[1:]):
                        perFrame2.loc[i, 'Trade'] = player.find("span").text.strip()

                assistDiv = soup.find_all('div', class_='table-cell assists')
                for i, player in enumerate(assistDiv[1:]):
                        perFrame2.loc[i, 'Assist'] = player.find("span").text.strip()   

                perFrame = perFrame._append(perFrame2, ignore_index=True)
                print(perFrame)

        if j == 4:
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))
                soup = BeautifulSoup(page_source, features='lxml')

                names = soup.find_all('span', class_="nickname")

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

        if j == 5:
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))
                soup = BeautifulSoup(page_source, features='lxml')

                names = soup.find_all('span', class_="nickname")

                for name in names:
                        aimFrame2 = aimFrame2._append({'Name': name.text.strip()}, ignore_index=True)

                headDiv = soup.find_all('div', class_='table-cell headshots current-sorting')
                for i, player in enumerate(headDiv[1:]):
                        aimFrame2.loc[i, 'Headshot'] = player.find("span").text.strip()

                headPerDiv = soup.find_all('div', class_='table-cell headshot_kills_accuracy')
                for i, player in enumerate(headPerDiv[1:]):
                        aimFrame2.loc[i, 'HeadshotPer'] = player.find("p").text.strip()

                shotDiv = soup.find_all('div', class_='table-cell shots')
                for i, player in enumerate(shotDiv[1:]):
                        aimFrame2.loc[i, 'Shot'] = player.find("span").text.strip()

                accDiv = soup.find_all('div', class_='table-cell accuracy')
                for i, player in enumerate(accDiv[1:]):
                        aimFrame2.loc[i, 'ShotPer'] = player.find("p").text.strip()  

                
                aimFrame = aimFrame._append(aimFrame2, ignore_index=True)
                print(aimFrame)

        if j == 6: 
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))
                
                soup = BeautifulSoup(page_source, features='lxml')

                names = soup.find_all('span', class_="nickname")

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

        if j == 7: 
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))
                
                soup = BeautifulSoup(page_source, features='lxml')

                names = soup.find_all('span', class_="nickname")

                for name in names:
                        gerFrame2 = gerFrame2._append({'Name': name.text.strip()}, ignore_index=True)

                nextDiv = soup.find_all('div', class_='table-cell flash_assist current-sorting')
                for i, player in enumerate(nextDiv[1:]):
                        gerFrame2.loc[i, 'FlashAssist'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell flash_blinded')
                for i, player in enumerate(nextDiv[1:]):
                        gerFrame2.loc[i, 'FlashBlind'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell flash_duration')
                for i, player in enumerate(nextDiv[1:]):
                        gerFrame2.loc[i, 'FlashDuration'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell molotov_damage')
                for i, player in enumerate(nextDiv[1:]):
                        gerFrame2.loc[i, 'MolDMG'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell he_damage')
                for i, player in enumerate(nextDiv[1:]):
                        gerFrame2.loc[i, 'HeDMG'] = player.find("span").text.strip() 

                gerFrame = gerFrame._append(gerFrame2, ignore_index=True)
                print(gerFrame)

        if j == 8: 
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))
                
                soup = BeautifulSoup(page_source, features='lxml')

                names = soup.find_all('span', class_="nickname")

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
    
        if j == 9: 
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))
                
                soup = BeautifulSoup(page_source, features='lxml')

                names = soup.find_all('span', class_="nickname")

                for name in names:
                        gunFrame2 = gunFrame2._append({'Name': name.text.strip()}, ignore_index=True)
                        
                nextDiv = soup.find_all('div', class_='table-cell ak47_kills current-sorting')
                for i, player in enumerate(nextDiv[1:]):
                        gunFrame2.loc[i, 'AK47-Kill'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell ak47_damage')
                for i, player in enumerate(nextDiv[1:]):
                        gunFrame2.loc[i, 'AK47-DMG'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell awp_kills')
                for i, player in enumerate(nextDiv[1:]):
                        gunFrame2.loc[i, 'AWP-Kill'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell awp_damage')
                for i, player in enumerate(nextDiv[1:]):
                        gunFrame2.loc[i, 'AWP-DMG'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell m4a1_kills')
                for i, player in enumerate(nextDiv[1:]):
                        gunFrame2.loc[i, 'M4A1-Kill'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell m4a1_damage')
                for i, player in enumerate(nextDiv[1:]):
                        gunFrame2.loc[i, 'M4A1-DMG'] = player.find("span").text.strip() 
                        
                gunFrame = gunFrame._append(gunFrame2, ignore_index=True)
                print(gunFrame)


        if j == 10: 
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))
                
                soup = BeautifulSoup(page_source, features='lxml')

                names = soup.find_all('span', class_="nickname")

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
                        
        if j == 11: 
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))
                
                soup = BeautifulSoup(page_source, features='lxml')

                names = soup.find_all('span', class_="nickname")

                for name in names:
                        pisFrame2 = pisFrame2._append({'Name': name.text.strip()}, ignore_index=True)
                        
                nextDiv = soup.find_all('div', class_='table-cell deagle_kills current-sorting')
                for i, player in enumerate(nextDiv[1:]):
                        pisFrame2.loc[i, 'Deagle-Kill'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell deagle_damage')
                for i, player in enumerate(nextDiv[1:]):
                        pisFrame2.loc[i, 'Deagle-DMG'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell glock_kills')
                for i, player in enumerate(nextDiv[1:]):
                        pisFrame2.loc[i, 'Glock-Kill'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell glock_damage')
                for i, player in enumerate(nextDiv[1:]):
                        pisFrame2.loc[i, 'Glock-DMG'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell usp_kills')
                for i, player in enumerate(nextDiv[1:]):
                        pisFrame2.loc[i, 'USP-Kill'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell usp_damage')
                for i, player in enumerate(nextDiv[1:]):
                        pisFrame2.loc[i, 'USP-DMG'] = player.find("span").text.strip()
                        
                pisFrame = pisFrame._append(pisFrame2, ignore_index=True)
                print(pisFrame)
    
    
        if j == 12: 
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))
                
                soup = BeautifulSoup(page_source, features='lxml')

                names = soup.find_all('span', class_="nickname")

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

        if j == 13: 
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))
                
                soup = BeautifulSoup(page_source, features='lxml')

                names = soup.find_all('span', class_="nickname")

                for name in names:
                        ecoFrame2 = ecoFrame2._append({'Name': name.text.strip()}, ignore_index=True)
                        
                nextDiv = soup.find_all('div', class_='table-cell kill_cost current-sorting')
                for i, player in enumerate(nextDiv[1:]):
                        ecoFrame2.loc[i, 'Kill-Cost'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell dmg_cost')
                for i, player in enumerate(nextDiv[1:]):
                        ecoFrame2.loc[i, 'DMG-Cost'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell saved')
                for i, player in enumerate(nextDiv[1:]):
                        ecoFrame2.loc[i, 'Saved-Avg'] = player.find("span").text.strip()
                        
                ecoFrame = ecoFrame._append(ecoFrame2, ignore_index=True)
                print(ecoFrame)
                        
                        
        if j == 14: 
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))
                
                soup = BeautifulSoup(page_source, features='lxml')

                names = soup.find_all('span', class_="nickname")

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
                        
                        
        if j == 15: 
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))
                
                soup = BeautifulSoup(page_source, features='lxml')

                names = soup.find_all('span', class_="nickname")

                for name in names:
                        killFrame2 = killFrame2._append({'Name': name.text.strip()}, ignore_index=True)
                
                nextDiv = soup.find_all('div', class_='table-cell multikills_vs_5 current-sorting')
                for i, player in enumerate(nextDiv[1:]):
                        killFrame2.loc[i, 'ACE'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell multikills_vs_4')
                for i, player in enumerate(nextDiv[1:]):
                        killFrame2.loc[i, '4Kill'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell multikills_vs_3')
                for i, player in enumerate(nextDiv[1:]):
                        killFrame2.loc[i, '3Kill'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell multikills_vs_2')
                for i, player in enumerate(nextDiv[1:]):
                        killFrame2.loc[i, '2Kill'] = player.find("span").text.strip()
                
                killFrame = killFrame._append(killFrame2, ignore_index=True)
                print(killFrame)
                        
                        
        if j == 16: 
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))
                
                soup = BeautifulSoup(page_source, features='lxml')

                names = soup.find_all('span', class_="nickname")

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

        if j == 17: 
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-cell')))
                
                soup = BeautifulSoup(page_source, features='lxml')

                names = soup.find_all('span', class_="nickname")

                for name in names:
                        cluFrame2 = cluFrame2._append({'Name': name.text.strip()}, ignore_index=True)
                
                nextDiv = soup.find_all('div', class_='table-cell clutches_vs_5 current-sorting')
                for i, player in enumerate(nextDiv[1:]):
                        cluFrame2.loc[i, '5v1'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell clutches_vs_4')
                for i, player in enumerate(nextDiv[1:]):
                        cluFrame2.loc[i, '4v1'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell clutches_vs_3')
                for i, player in enumerate(nextDiv[1:]):
                        cluFrame2.loc[i, '3v1'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell clutches_vs_2')
                for i, player in enumerate(nextDiv[1:]):
                        cluFrame2.loc[i, '2v1'] = player.find("span").text.strip()

                nextDiv = soup.find_all('div', class_='table-cell clutches_vs_1')
                for i, player in enumerate(nextDiv[1:]):
                        cluFrame2.loc[i, '1v1'] = player.find("span").text.strip()
                        
                cluFrame = cluFrame._append(cluFrame2, ignore_index=True)
                print(cluFrame)
                
                
dfs = [mainFrame, perFrame, killFrame, aimFrame, cluFrame, gerFrame, gunFrame, pisFrame]

merged_df = pd.concat([df.set_index('Name') for df in dfs], axis=1, join='outer').reset_index()

merged_df.to_csv('cs_atier_data.csv', index=False)

driver.quit()