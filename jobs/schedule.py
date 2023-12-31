import pandas as pd
from core.diretta import Diretta

scraper = Diretta()
scraper.get_schedule(days=3).to_csv('/home/larrys-linux/betblaze/data/schedule_.csv', index=None)