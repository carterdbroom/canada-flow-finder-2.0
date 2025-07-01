from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
station_ids = []

# Reads station IDs from a text file and stores them in a list
with open ('stations.txt', 'r') as f:
    for station_id in f: 
        station_ids.append(station_id.strip())

# Navigates to the first station's page, which requires agreement to a disclaimer
driver.get(f'https://wateroffice.ec.gc.ca/report/real_time_e.html?stn={station_ids[0]}')
# Finds the agreement button and clicks it        
agreement_button = driver.find_element(By.XPATH, '//input[@value="I Agree" and @name="disclaimer_action"]')
agreement_button.click()

# Finds the download link by its text and clicks it
download_link = driver.find_element(By.LINK_TEXT, 'Download?')
download_link.click()  

# Opens the Water Office website to download data for each station ID
for i in range(1, len(station_ids)):
    # Navigates to the station's page
    driver.get(f'https://wateroffice.ec.gc.ca/report/real_time_e.html?stn={station_ids[i]}')
    
    # Finds the download link by its text and clicks it
    download_link = driver.find_element(By.LINK_TEXT, 'Download?')
    download_link.click()  

    # Finds the correct discharge header
    #discharge_header = driver.find_element(By.XPATH, '//h2[contains(text(), "Discharge (unit values)")]')

    #discharge_csv_link = discharge_header.find_element(By.XPATH, 
