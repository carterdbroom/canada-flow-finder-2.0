from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import timeit

# Running in headless mode and disabling images to speed up the process
chrome_options = Options()
chrome_options.add_argument('--headless=new')
prefs = {'profile.managed_default_content_settings.images': 2}
chrome_options.add_experimental_option('prefs', prefs)  

driver = webdriver.Chrome(options=chrome_options)
station_ids = []
stations_with_no_data = []

# Reads station IDs from a text file and stores them in a list
with open ('stations.txt', 'r') as f:
    for station_id in f: 
        station_ids.append(station_id.strip())

start = timeit.default_timer()
# Navigates to the first station's page, which requires agreement to a disclaimer
driver.get(f'https://wateroffice.ec.gc.ca/report/real_time_e.html?stn={station_ids[0]}')
# Finds the agreement button and clicks it        
agreement_button = driver.find_element(By.XPATH, '//input[@value="I Agree" and @name="disclaimer_action"]')
agreement_button.click()

try: 
    # Finds the download link by its text and clicks it
    correct_section = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Download?")]')))
    download_link = driver.find_element(By.LINK_TEXT, 'Download?')
    download_link.click() 
except TimeoutException: 
    elapsed = timeit.default_timer() - start
    print(f'Cannot find download link for station: {station_ids[0]}, {elapsed}')

try:
    # Finds the csv discharge link and clicks it
    # Note: The XPATH may need to be adjusted if the structure of the page changes
    correct_main = driver.find_element(By.XPATH, '//main[@property="mainContentOfPage"]')
    correct_div = correct_main.find_element(By.XPATH, './div[2]')
    correct_section = correct_div.find_element(By.XPATH, './section[2]')
    discharge_link = correct_section.find_element(By.XPATH, './/a[contains(@href, "report_e.html") and contains(@href, "df=csv")]')
    discharge_link.click()
    elapsed = timeit.default_timer() - start
    print(f'Found data for station: {station_ids[0]}, {elapsed}')
except TimeoutException:
    elapsed = timeit.default_timer() - start
    print(f'Cannot find discharge data for station: {station_ids[0]}, {elapsed}')
    stations_with_no_data.append(station_ids[0])

# Opens the Water Office website to download data for each station ID
for i in range(1, len(station_ids)):
    
    start = timeit.default_timer()

    # Navigates to the station's page
    driver.get(f'https://wateroffice.ec.gc.ca/report/real_time_e.html?stn={station_ids[i]}')
    
    try: 
        # Finds the download link by its text and clicks it
        correct_section = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Download?")]')))
        download_link = driver.find_element(By.LINK_TEXT, 'Download?')
        download_link.click() 
    except TimeoutException: 
        elapsed = timeit.default_timer() - start
        print(f'Cannot find download link for station: {station_ids[i]}, {elapsed}')
        continue
    
    # In case there isn't data for the discharge, we check for the presence of the discharge header
    try: 
        # Finds the csv discharge link and clicks it
        # Note: The XPATH may need to be adjusted if the structure of the page changes
        correct_section = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Discharge (unit values)")]')))

        correct_main = driver.find_element(By.XPATH, '//main[@property="mainContentOfPage"]')
        correct_div = correct_main.find_element(By.XPATH, './div[2]')
        correct_section = correct_div.find_element(By.XPATH, './section[2]')
        discharge_link = correct_section.find_element(By.XPATH, './/a[@href="/download/report_e.html?dt=47&df=csv&ext=zip"]')
        discharge_link.click()
        elapsed = timeit.default_timer() - start
        print(f'Found data for station: {station_ids[i]}, {elapsed}')
    except TimeoutException:
        elapsed = timeit.default_timer() - start
        print(f'Cannot find discharge data for station: {station_ids[i]}, {elapsed}')
        stations_with_no_data.append(station_ids[i])
        continue    

driver.close()