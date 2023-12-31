import pandas as pd
from datetime import datetime
from core.diretta import Diretta

scraper = Diretta()

schedule_ = pd.read_csv("/home/larrys-linux/betblaze/data/schedule_.csv")
schedule_['datetime'] = pd.to_datetime(schedule_.datetime)

filename = f"odds_{datetime.now().strftime('%T')}.csv"
scraper.scrape_odds(schedule_, in_program=True).to_csv(f"/home/larrys-linux/betblaze/data/ts/{filename}", index=None)