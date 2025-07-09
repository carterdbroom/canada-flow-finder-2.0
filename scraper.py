from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import timeit
import os
import shutil

def scraper():
    try: 
        # Creating a temporary directory that will delete itself after the script runs or is interrupted
        CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
        TEMP_DIRECTORY = os.path.join(CURRENT_DIRECTORY, 'temp_dir')
        os.makedirs(TEMP_DIRECTORY, exist_ok=True)
        print(f'Download directory: {TEMP_DIRECTORY}')   
        # Running in headless mode and disabling images to speed up the process
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')

        # Disables the loading of images, speeds up scraping
        # Downloades files automatically
        # Allows custom download directory
        # Setting custom download directory
        prefs = {'profile.managed_default_content_settings.images': 2, 'download.prompt_for_download': False, 'download.directory_upgrade': True, 'download.default_directory': TEMP_DIRECTORY }
        chrome_options.add_experimental_option('prefs', prefs)  

        # Initializing the WebDriver
        driver = webdriver.Chrome(options=chrome_options)

        # Initializing lists that will hold relevant station information
        station_ids = []
        stations_with_no_data = []

        total_start = timeit.default_timer()

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
            correct_page = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Discharge (unit values)")]')))

            correct_main = driver.find_element(By.XPATH, '//main[@property="mainContentOfPage"]')
            correct_div = correct_main.find_element(By.XPATH, './div[2]')
            correct_header = correct_div.find_element(By.XPATH, './/h2[contains(text(), "Discharge (unit values)")]')
            following_div = correct_header.find_element(By.XPATH, './following-sibling::div')
            discharge_link = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, './/a[@href="/download/report_e.html?dt=47&df=csv&ext=zip"]')))
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
            
            try: 
                # Finds the csv discharge link and clicks it
                # Note: The XPATH may need to be adjusted if the structure of the page changes
                correct_page = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Discharge (unit values)")]')))

                correct_main = driver.find_element(By.XPATH, '//main[@property="mainContentOfPage"]')
                correct_div = correct_main.find_element(By.XPATH, './div[2]')
                correct_header = correct_div.find_element(By.XPATH, './/h2[contains(text(), "Discharge (unit values)")]')
                following_div = correct_header.find_element(By.XPATH, './following-sibling::div') 
                discharge_link = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, './/a[@href="/download/report_e.html?dt=47&df=csv&ext=zip"]')))
                discharge_link.click()
                elapsed = timeit.default_timer() - start 
                print(f'Found data for station: {station_ids[i]}, {elapsed}')

            except TimeoutException:
                elapsed = timeit.default_timer() - start
                print(f'Cannot find discharge data for station: {station_ids[i]}, {elapsed}')
                stations_with_no_data.append(station_ids[i])
                continue    

        with open ('no_station_data.txt', 'w') as f:
            for station in stations_with_no_data: 
                f.write(f'{station}\n')

        total_elapsed = timeit.default_timer() - total_start
        print(f'Total time elapsed: {total_elapsed}')

        shutil.rmtree(TEMP_DIRECTORY)
        print("Deleted directory")
        driver.quit()
    finally: 
        if os.path.exists(TEMP_DIRECTORY): 
            shutil.rmtree(TEMP_DIRECTORY)
            print("Deleted directory")