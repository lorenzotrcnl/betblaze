''' GET 3-days PROGRAMMED MATCHES'''
import sys
sys.path.append('/home/betblaze')

import pandas as pd
from core.diretta import Diretta

scraper = Diretta()
scraper.get_schedule(days=3).to_csv('../data/schedule_.csv', index=None)