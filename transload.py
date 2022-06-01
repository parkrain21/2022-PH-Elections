import csv
import os
from bs4 import BeautifulSoup
import logging

# Transform and Load process
def wrangle(webpage):
    if webpage == None:
        row = ''
    else:
        soup = BeautifulSoup(webpage, 'lxml')

        x = soup.find_all('div', class_='col-xs-7 no-side-padding gen-inf-label ng-binding')
        y = soup.find_all('div', class_='col-xs-5 no-side-padding gen-inf-value ng-binding')

        common_info = {k.text.strip():v.text.strip() for k,v in zip(x[:10],y[:10])}

        result = soup.find_all('div', class_='candidate-result')
        result = [c.text.strip() for c in result[:780]]

        # 0-10 Presidents
        # 11-19 VP
        # 20-83 Senators
        # 84+ Partylist
        national_results = {k:v for k,v in zip(result[::3], result[1::3])}
        row = {**common_info, **national_results}

    return row


def create_csv(filename, headers):
    if filename[-3:] != 'csv':
        filename += '.csv'
    
    with open(filename, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()


def store_data(filename, row):  
    # Check if file doesn't exist, if not then create it.
    colnames = row.keys()
    if filename not in os.listdir():
        create_csv(filename, colnames)

    with open(filename, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=colnames)
        writer.writerow(row)

def store_blank(filename, code):
    with open(filename, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['','','',code])