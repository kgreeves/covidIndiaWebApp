import pandas as pd
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent

indian_states = pd.read_json(str(BASE_PATH)+'\\data\\states.json')
indian_covid_json = pd.read_json(str(BASE_PATH)+'\\data\\state_district_wise.json')

is_states = list(indian_states['features'].keys())
icj_states = list(indian_covid_json.keys())

print(is_states)
print(icj_states)
print(indian_states['features'])

for state in is_states:

    curr_state = indian_states['features'][state]['id']
    if curr_state in indian_covid_json.keys():
        print(indian_states['features'][state]['properties'])
        indian_states['features'][state]['properties']['covid'] = indian_covid_json[curr_state]
        print(indian_states['features'][state]['properties'])
    else:
        print(f'{curr_state} is not in both.')