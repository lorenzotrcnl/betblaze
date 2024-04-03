'''
IN      > 
Reach diretta.it and get all scheduled matches ids to construct the urls.

OUT     < 
A .csv file containing all ids and other details.
'''

import re
import requests
import pandas as pd

headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'dnt': '1',
        'origin': 'https://www.diretta.it',
        'referer': 'https://www.diretta.it/',
        'sec-ch-ua': '"Chromium";v="123", "Not:A-Brand";v="8"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-fsign': 'SW9D1eZo'
    }
base_url = 'https://local-it.flashscore.ninja/400/x/feed/f_1_{day}_1_it_1'
allmatches = []

for day in range(1,6):

    url = base_url.format(day=day)
    response = requests.get(url, headers=headers)
    matches = re.findall(r'AA÷(.*?)¬', response.text)

    allmatches.extend([match_id for match_id in matches])
    print(f"{day}, {len(matches)}")

pd.DataFrame(allmatches, columns=['match_id']).to_csv('./data/ids.csv')
print("IDs saved.")