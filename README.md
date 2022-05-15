# 2022-PH-Elections
9 May 2022 - Philippine National Elections webscraper using Selenium (Python)

You can access the COMELEC Transparency server [here](https://2022electionresults.comelec.gov.ph/#/er/0/).

#### Modules used:
- Selenium
- BeautifulSoup4
- pandas
- csv
- os
- time

#### Instructions:
1. Just run the 'elections_extract.py' on your terminal
2. The data would automatically be populated on a csv file named 'elections.csv'

#### Known errors to be addressed:
- ETL process is quite slow (still unsure if I could speed this up?)
- Generates some blank records (fails to parse the HTML data)
- Some sleep timings are off, will look for optimal values so errors would not arise.
