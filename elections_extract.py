from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from elections_transload import wrangle
import pandas as pd
import time

url = 'https://2022electionresults.comelec.gov.ph/#/er/0/'
driver = webdriver.Edge()
i = 0
j = 0
k = 0
l = 0
m = 0

df = pd.DataFrame()

driver.get(url)
action = ActionChains(driver)
driver.maximize_window()
# driver.execute_script("document.body.style.zoom='90%'")
# driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(1)

def elections():
    global i,j,k,l

    rlen = interact_dropdowns(2)
    down_enter_delayed(i)
    time.sleep(0.3)

    # Provinces
    plen = interact_dropdowns(3)
    down_enter_delayed(j)
    time.sleep(0.3)

    # Cities
    clen = interact_dropdowns(4)
    down_enter_delayed(k)
    time.sleep(0.3)

    # Baranggays
    blen = interact_dropdowns(5)
    down_enter_delayed(l)
    time.sleep(0.3)
    
    return rlen, plen, clen, blen

def precinct():
    global i,j,k,l,m
    while True:
        rlen, plen, clen, blen = elections()
        prlen = interact_dropdowns(6)
        down_enter_delayed(m)
        time.sleep(3)

        wrangle(driver.page_source)
        time.sleep(1)

        driver.refresh()
        time.sleep(2)

        print(f'Region: {i+1}/{rlen} | Province: {j+1}/{plen} | City: {k+1}/{clen} | Brgy: {l+1}/{blen} | Prec: {m+1}/{prlen}')
    # Incrementing the index variables
        m+=1
        if m == prlen:      # If Precinct length is at the end
            m = 0           # Reset precinct index
            l += 1          # Increment Baranggay

        if l == blen:       # Baranggay Length
            l = 0           # Reset brgy index
            k += 1          # Increment City/Municipality

        if k == clen:       # City Length
            k = 0           # Reset city index
            j += 1          # Increment province

        if j == plen:       # Province Length
            j = 0           # Reset province index
            i += 1          # Increment REGION 

        if i == rlen:       # Region Length
            break

# ------------------------------------------------------- #        

def interact_dropdowns(n):
    if n not in (2,3,4,5,6):
        raise ValueError

    # Expand the drop down menu
    driver.find_element(By.XPATH, f'//*[@id="container"]/ui-view/div/div/div[1]/nav/div/ul/li/div[5]/div[{n}]/nav-filter/div/span/div/div/span/span').click()
    
    # Get all the list items on the dropdown menu
    elements = driver.find_element(By.XPATH, f'//*[@id="container"]/ui-view/div/div/div[1]/nav/div/ul/li/div[5]/div[{n}]/nav-filter/div/span/div/div/div[2]/ul').find_elements(By.TAG_NAME, 'li')
    n = len(elements)
    return n

def down_enter_delayed(n):
    for _ in range(n):
        action.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.3)
    action.send_keys(Keys.ENTER)
    action.perform()


if __name__ == '__main__':
    precinct()

    