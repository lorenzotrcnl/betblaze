''' GET 3-days PROGRAMMED MATCHES'''
import sys
sys.path.append('/Users/lorenzotarcinale/repo/diretta-scraper')

import pandas as pd
from datetime import datetime
from scraper.diretta import Diretta

scraper = Diretta()

schedule_ = pd.read_csv("../data/schedule_.csv")
schedule_['datetime'] = pd.to_datetime(schedule_.datetime)

filename = f"closings_{datetime.now().strftime('%d-%m')}.csv"
scraper.scrape_odds(schedule_, in_program=False).to_csv(f"../data/closing/{filename}", index=None)