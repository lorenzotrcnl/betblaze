import sys
sys.path.append('/home/larrys-linux/betblaze')

import pandas as pd
from datetime import datetime
from core.diretta import Diretta

scraper = Diretta()

schedule_ = pd.read_csv("/home/larrys-linux/betblaze/data/schedule_.csv")
schedule_['datetime'] = pd.to_datetime(schedule_.datetime)

filename = f"closings_{datetime.now().strftime('%d-%m')}.csv"
scraper.scrape_odds(schedule_, in_program=False).to_csv(f"/home/larrys-linux/betblaze/data/closings/{filename}", index=None)