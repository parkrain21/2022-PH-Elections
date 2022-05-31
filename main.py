from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from transload import wrangle, store_data
import pandas as pd
import time
import logging

# ----------------------SETUP---------------------------- # 

logging.basicConfig(filename="elections.log", 
					format='[%(levelname)s]:  %(message)s', 
					level=logging.INFO) 

url = 'https://2022electionresults.comelec.gov.ph/#/er/0/'
driver = webdriver.Edge()

df = pd.DataFrame()

driver.get(url)
driver.implicitly_wait(15)
action = ActionChains(driver)

# ------------------PROGRAM CODE-------------------------- # 

def get_precinct_codes():
    codes = pd.read_excel('2022NLEPOP.xlsx')
    codes = codes['PRECINCT_ID'].astype(str).str.zfill(8)
    return codes.to_list()

def main():
    precinct_codes = get_precinct_codes()

    i = 275      #edit this for manual config

    # I used while loop for automatic retry
    while i < len(precinct_codes):
        try:
            start_time = time.time()
            driver.find_element_by_xpath('//*[@title="Search clustered precinct"]').click()
            time.sleep(0.5)
            active_ele = driver.switch_to.active_element
            active_ele.send_keys(precinct_codes[i])
            active_ele.send_keys(Keys.ENTER)
            time.sleep(2)

            # check if there are no ERs received
            na = driver.find_element(By.XPATH, '//*[@id="container"]/ui-view/div/div/div[2]/div[2]/div[2]/results-viewer/div/div/div/span').text
            if na == 'No ER received yet for this Clustered Precinct':
                print(f"{na} | index {i}, pcode: {precinct_codes[i]} | elapsed time: {round(time.time()-start_time,2)} secs.")
                logging.info(f"{na} | index {i}, pcode: {precinct_codes[i]} | elapsed time: {round(time.time()-start_time,2)} secs.")
                i += 1
                store_data('test.csv', '\n') 

            # If data is available
            else:   
                content = driver.page_source
                row = wrangle(content)      # I did not change the parameters, fix this

                if len(row) == 270:
                    store_data('test.csv', row)
                    print(f"{len(row)} entries added on index {i}, pcode: {precinct_codes[i]} | elapsed time: {round(time.time()-start_time,2)} secs.")
                    logging.info(f"{len(row)} entries added on index {i}, pcode: {precinct_codes[i]} | elapsed time: {round(time.time()-start_time,2)} secs.")
                    i += 1
                else:
                    print(f"Incomplete records, only {len(row)} entries fetched for index {i}, pcode {precinct_codes[i]}. Retrying...")
                    logging.warning(f"Incomplete records, only {len(row)} entries fetched for index {i}, pcode {precinct_codes[i]}. Retrying...")
        except:
            pass
        
        time.sleep(0.75)

if __name__ == '__main__':
    main()