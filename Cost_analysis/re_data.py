import requests
import pandas as pd
import json

coordinates = pd.read_excel('Data/PV_WIND_50_Punkte.xlsx', sheet_name='PV_Punkte')
df_electricity = pd.read_csv('Data/pv_wind_electricity.csv', index_col=0)
df_electricity.reset_index(drop=True, inplace=True)
#df_electricity = pd.DataFrame()

token = 'ab3c6a38f8ad704e00fb3e2ee7e7584c36f8c078'     #Pascal
#token = '1aa2a150a835fa055ee06eb84e96d5302222612d'      #Max
#token = '7cdfd4e7524e7ffe4490467156f20725f8e3d666'     #Soufiane
api_base = 'https://www.renewables.ninja/api/'

s = requests.session()
# Send token header with each request
s.headers = {'Authorization': 'Token ' + token}

url_pv = api_base + 'data/pv'
url_wind = api_base + 'data/wind'

for i in range(1):   # Nur sechs Anfragen pro Min (2*3), um API-Limits zu beachten: Maximal 50 pro Stunden
    lat = coordinates.at[i, 'Latitude']
    lon = coordinates.at[i, 'Longitude']
    # PV
    args_pv = {
        'lat': lat,
        'lon': lon,
        'date_from': '2019-01-01',
        'date_to': '2019-12-31',
        'dataset': 'merra2',
        'capacity': 1.0,
        'system_loss': 0.1,
        'tracking': 0,
        'tilt': 35,
        'azim': 180,
        'format': 'json'
    }

    r_pv = s.get(url_pv, params=args_pv)
    parsed_response_pv = json.loads(r_pv.text)
    data_pv = pd.read_json(json.dumps(parsed_response_pv['data']), orient='index')
    metadata_pv = parsed_response_pv['metadata']

    #Wind
    args_wind = {
        'lat': lat,
        'lon': lon,
        'date_from': '2019-01-01',
        'date_to': '2019-12-31',
        'capacity': 1.0,
        'height': 150,
        'turbine': 'Vestas V136 3450',
        'format': 'json'
    }

    r_wind = s.get(url_wind, params=args_wind)
    parsed_response_wind = json.loads(r_wind.text)
    data_wind = pd.read_json(json.dumps(parsed_response_wind['data']), orient='index')
    metadata_wind = parsed_response_wind['metadata']

    data_pv.rename(columns={'electricity': f'electricity_PV_{i}'}, inplace=True)
    data_wind.rename(columns={'electricity': f'electricity_Wind_{i}'}, inplace=True)

    df_concat = pd.concat([data_pv, data_wind], axis=1)
    df_concat.reset_index(drop=True, inplace=True)
    df_electricity = pd.concat([df_electricity, df_concat], axis=1)

#df_electricity.to_csv('pv_wind_electricity.csv')