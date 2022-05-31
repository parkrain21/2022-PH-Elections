# 2022-PH-Elections
31 May 2022 - Philippine National Elections webscraper using Selenium (Python)

You can access the COMELEC Transparency server [here](https://2022electionresults.comelec.gov.ph/#/er/0/).

#### Modules used:
- Selenium
- BeautifulSoup4
- pandas
- csv
- os
- time

#### Instructions:
1. Just run the 'main.py' on your terminal and the csv file will be generated.
2. There are some records that do not have existing ERs, so those are not included in the csv file.
3. Will try to save those in a separate file, for the meantime it is all in the log files.

#### Known errors to be addressed:
- Old script takes 30+ seconds to 3 seconds average (as of 31 May 2022)
