import pandas as pd
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Diretta:
    def __init__(self) -> None:
        pass

    
    def initialize_driver(self):
        # initialize the driver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--log-level=3")
        chrome_options.binary_location = "/usr/bin/google-chrome"
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)


    def get_schedule(self, url="https://www.diretta.it/", days=3, waiting_seconds=5):
        """
        Get match codes from the given website.

        Parameters:
        - url (str): The URL of the website to scrape.
        - waiting_seconds (int): Maximum wait time for elements to appear.

        Returns:
        - list: List of match codes.
        """

        ## Set up Chrome options for a headless browser
        #chrome_options = Options()
        #chrome_options.add_argument("--headless")
        #self.driver = webdriver.Chrome(options=chrome_options)
        self.initialize_driver()

        # Open the provided URL
        print(f"Getting matches ID from {url}")
        self.driver.get(url)

        # Wait for the main table container to load
        wait = WebDriverWait(self.driver, waiting_seconds)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'container__livetable')))

        # Scroll down to reveal the 'Programma' filter
        self.driver.execute_script("window.scrollBy(0, 100);")

        # Click on 'Programma' filter
        self.driver.find_element(By.XPATH, "//div[@class='filters__text filters__text--default' and text()='Programma']").click()

        # Get match codes for the next _ days
        match_codes = []
        for i in range(0, days):
            # Get match IDs on the current page
            match_elements = self.driver.find_elements(By.CLASS_NAME, "event__match")
            match_ids = [element.get_attribute("id") for element in match_elements]
            print(f"Page {i+1}, total matches to get = {len(match_ids)}")

            for match_id in match_ids:
                # Click on each match to open a new window
                wait.until(EC.element_to_be_clickable((By.ID, match_id)))
                self.driver.execute_script(f"document.getElementById('{match_id}').click();")

                # Wait for a new window to open
                wait.until(EC.number_of_windows_to_be(2))

                # Switch to the new window
                window_handles = self.driver.window_handles
                self.driver.switch_to.window(window_handles[1])

                # Get the current URL (containing match code), match date and close the new window
                match_date = self.driver.find_elements(By.CLASS_NAME, "duelParticipant__startTime")
                match_date = [date.text for date in match_date][0]
                match_codes.append([self.driver.current_url, match_date])
                self.driver.close()

                # Switch back to the original window
                self.driver.switch_to.window(window_handles[0])

            # Go to the next day
            self.driver.find_element(By.CLASS_NAME, 'calendar__navigation--tomorrow').click()
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "event__match")))
        
        # Quit the browser
        self.driver.quit()

        # Extract match codes from URLs
        codesDF = pd.DataFrame(match_codes, columns=['code', 'datetime'])
        codesDF['code'] = [link.split("/")[4] for link in codesDF.code]
        codesDF['datetime'] = pd.to_datetime(codesDF.datetime, dayfirst=True)
        codesDF.sort_values(['datetime'], inplace=True)

        print("Done!")
        return codesDF

    
    def extract_bookmaker(self, row):
        """
        Extracts the bookmaker name from a table row.
    
        Parameters:
            row (bs4.element.Tag): BeautifulSoup Tag representing a table row.
    
        Returns:
            str: Bookmaker name or 'N/A' if not found.
        """
        bookmaker_element = row.select_one('.oddsCell__bookmakerPart .oddsCell__bookmakerCell a')
        return bookmaker_element.get('title') if bookmaker_element else 'N/A'
    

    def extract_odds(self, row):
        """
        Extracts the total and odds values from a table row.

        Parameters:
            row (bs4.element.Tag): BeautifulSoup Tag representing a table row.

        Returns:
            tuple: Total and a list of odds values.
        """
        odds_elements = row.select('.oddsCell__odd')

        if not odds_elements:
            odds_elements = row.select('.oddsCell__noOddsCell')
            odds = [odd.text for odd in odds_elements]

            #total = odds_elements[0].text
            #odds = [odd.text for odd in odds_elements[1:]]
        else:
            odds = []
            try:
                odds = [row.select_one('.oddsCell__noOddsCell').text]
            except:
                pass
            
            odds = odds + [odd.text for odd in odds_elements]

        return odds


    def get_page_source(self, schedule, odds_type='quote-1x2'):
        self.initialize_driver()
        sources = []                                       # -----------> array of page source and datetime of event

        for match_code, date in zip(schedule.code, schedule.datetime):
            url = f"https://www.diretta.it/partita/{match_code}/#/comparazione-quote/{odds_type}/finale"
            print(f"Getting {url}")
            self.driver.get(url)

            if self.driver.current_url.endswith("finale"): # -----------> odds available
                try:
                    # Wait for the odds table to load and get the page source
                    self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'oddsTab__tableWrapper')))
                    sources.append([self.driver.page_source, date])
                except TimeoutException as e:
                    print("Timeout!")
            else:
                print(f"odds not available for {match_code}")

        print("Done!")
        self.driver.quit()
        return pd.DataFrame(sources, columns=['source', 'datetime'])


    def get_odds(self, htmls):
        ''' '''
        if len(htmls) == 0:
            return None
        
        print(f"scraping {len(htmls)} matches...")

        odds_data = []

        for html in htmls:
            # Parse the HTML page source using BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            # Get the league name
            league = soup.find('span', class_='tournamentHeader__country').text.strip()

            # Get the participants of the match
            teams_table = soup.find('div', class_='duelParticipant').select('.participant__participantName')
            teams = list(set([team.text for team in teams_table]))
            match = f"{teams[0]} - {teams[1]}"

            # Get the match date
            date = soup.find('div', class_='duelParticipant__startTime').div.text.strip()

            # Get the match score ('-' if match not played yet)
            # Find the element with class 'detailScore__wrapper' and extract the text
            score = soup.find('div', class_='detailScore__wrapper').get_text(strip=True)

            # get the record timestamp
            timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            # Check for the presence of the odds table
            odds_table = soup.find('div', class_='oddsTab__tableWrapper')
            if odds_table:
                # Find all rows in the table body
                rows = odds_table.select('.ui-table__body .ui-table__row')

                # Loop through each row and extract information
                for row in rows:
                    bookmaker = self.extract_bookmaker(row)
                    odds_values = self.extract_odds(row)
                    odds_data.append([timestamp, league, match, date, score, bookmaker] + odds_values)

        # Create a DataFrame from the collected data
        header = [header.text.strip() for header in odds_table.find_all('div', class_='ui-table__headerCell')]
        seen = set()
        header = [x for x in header if x not in seen and not seen.add(x)]
        columns = ['timestamp','league','match','date','score'] + header

        print("Done!")
        return pd.DataFrame(odds_data, columns=columns)


    def scrape_odds(self, schedule, in_program=True):
        ''' Choose to get odds of future matches or get results of past matches + closing odds '''

        htmls = self.get_page_source(schedule)              # -----------> page_source di tutti i match
        if in_program: return self.get_odds(htmls[htmls.datetime>datetime.now()].source) # -----------> odds dei match in programma
        else: return self.get_odds(htmls[htmls.datetime<datetime.now()].source)          # -----------> closing odds + result dei match giocati