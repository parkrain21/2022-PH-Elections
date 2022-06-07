from distutils.log import info
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from transload import wrangle, store_data, store_blank
import pandas as pd
import time
import logging

# ----------------------SETUP---------------------------- # 

logging.basicConfig(filename="elections.log", 
					format='[%(levelname)s]:  %(message)s', 
					level=logging.INFO) 

i = 0      #edit this for manual config

def launch_driver():
    url = 'https://2022electionresults.comelec.gov.ph/#/er/0/'
    driver = webdriver.Edge()
    driver.get(url)
    driver.implicitly_wait(15)
    return driver

# ------------------PROGRAM CODE-------------------------- # 

def get_precinct_codes():
    codes = pd.read_excel('2022NLEPOP.xlsx')
    codes = codes['PRECINCT_ID'].astype(str).str.zfill(8)
    return codes.to_list()

def main():
    global i

    # Initialize the list of precinct codes
    precinct_codes = get_precinct_codes()
    driver = launch_driver()

    # While loop for automatic retry in case it fails
    while i < len(precinct_codes):
        # Try to reinitialize the webdriver object every 200 records to avoid out of memory error
        if i % 200 == 0:
            driver.close()
            time.sleep(2)
            print("Reinitializing webdriver to avoid memory leaks")
            logging,info("Reinitialized webdriver to avoid memory leaks")
            driver = launch_driver()

        try:
            # Input precinct id, and wait for results to load
            start_time = time.time()
            driver.find_element(By.XPATH, '//*[@title="Search clustered precinct"]').click()
            time.sleep(0.5)
            active_ele = driver.switch_to.active_element
            active_ele.send_keys(precinct_codes[i])
            active_ele.send_keys(Keys.ENTER)
            time.sleep(3.8)

            # check if there are no ERs received
            content = driver.page_source
            soup = BeautifulSoup(content, 'lxml')
            na = soup.body.find(text='No ER received yet for this Clustered Precinct')

            if na:
                print(f"{na.text} | index {i}, pcode: {precinct_codes[i]} | elapsed time: {round(time.time()-start_time,2)} secs.")
                logging.info(f"{na.text} | index {i}, pcode: {precinct_codes[i]} | elapsed time: {round(time.time()-start_time,2)} secs.")
                i += 1
                store_blank('elections.csv', precinct_codes[i]) 

            # If ER data is available
            else:   
                row = wrangle(content) 

                if len(row) == 270:
                    store_data('elections.csv', row)
                    print(f"{len(row)} entries added on index {i}, pcode: {precinct_codes[i]} | elapsed time: {round(time.time()-start_time,2)} secs.")
                    logging.info(f"{len(row)} entries added on index {i}, pcode: {precinct_codes[i]} | elapsed time: {round(time.time()-start_time,2)} secs.")
                    i += 1
                else:
                    print(f"Incomplete records, only {len(row)} entries fetched for index {i}, pcode {precinct_codes[i]}. Retrying...")
                    logging.warning(f"Incomplete records, only {len(row)} entries fetched for index {i}, pcode {precinct_codes[i]}. Retrying...")
                    time.sleep(2)
        except:
            pass

if __name__ == '__main__':
    main()