import json
import requests
import pandas as pd
from datetime import datetime

# Initialize a session
session = requests.Session()

# Define the base URL and read match IDs
url = 'https://400.ds.lsapp.eu/pq_graphql'
match_ids = pd.read_csv('./data/ids.csv')['match_id']

data = []
total_ids = len(match_ids)
invalid_matches = []

try:
    for index, id_ in enumerate(match_ids, start=1):
        # Base parameters
        base_params = {
            'eventId': id_,
            'projectId': '400'
        }

        # Information request
        info_params = {'_hash': 'dsof', **base_params}
        try:
            info_response = session.get(url, params=info_params)
            info_response.raise_for_status()  # Raises an HTTPError if the response was an error
            infoJSON = info_response.json()

            # Odds request
            odds_params = {
                '_hash': 'ope',
                'geoIpCode': 'IT',
                'geoIpSubdivisionCode': 'IT72',
                **base_params
            }
            odds_response = session.get(url, params=odds_params)
            odds_response.raise_for_status()
            oddsJSON = odds_response.json()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            continue

        dataODDS = {}
        for bm in oddsJSON.get('data', {}).get('findPrematchOddsById', {}).get('odds', []):
            try:
                dataODDS[bm['bookmakerId']] = {
                    'X': bm['odds'][0]['value'],
                    'XOP': bm['odds'][0]['opening'],
                    '1': bm['odds'][1]['value'],
                    '1OP': bm['odds'][1]['opening'],
                    '2': bm['odds'][2]['value'],
                    '2OP': bm['odds'][2]['opening']
                }
            except (IndexError, KeyError) as e:
                #print(f"Error processing odds data for match {id_}: {e}")
                continue

        if len(dataODDS) < 3:
            invalid_matches.append(id_)
            print(f"[{index}/{total_ids}] {id_} invalid")
            continue

        # Final dict
        try:
            dataFINAL = {
                id_: {
                    'home_team': infoJSON['data']['findEventById']['eventParticipants'][0]['name'],
                    'away_team': infoJSON['data']['findEventById']['eventParticipants'][1]['name'],
                    'startTime': infoJSON['data']['findEventById']['eventParticipants'][0]['participants'][0]['participant']['nextEvents'][0]['startTime'],
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'odds': dataODDS
                }
            }
        except (IndexError, KeyError) as e:
            #print(f"Error processing final data for match {id_}: {e}")
            continue

        data.append(dataFINAL)

        print(f"[{index}/{total_ids}] {id_}")

except KeyboardInterrupt:
    print("Script interrupted. Saving current progress...")

finally:
    print("Removing invalid matches from the file.")
    pd.DataFrame(list(set(match_ids) - set(invalid_matches)), columns=['match_id']).to_csv('./data/ids.csv')
    print("Match IDs file updated!")

    print("Saving odds data.")
    with open(f'./data/odds_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.json', 'w') as f:
        json.dump(data, f, indent=4)
    print("File saved!")
