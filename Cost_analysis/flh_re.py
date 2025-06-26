import pandas as pd

df_re = pd.read_csv('Data/pv_wind_electricity.csv')
df_re = df_re.drop(columns= ['Unnamed: 0'])

ds_sum = df_re.sum()

df_flh = pd.DataFrame(columns=['FLH_PV', 'FLH_Wind'])
for i in range(0,50):
    pv = ds_sum[f'electricity_PV_{i}']
    wind = ds_sum[f'electricity_Wind_{i}']

    df_flh.at[i, 'FLH_PV'] = pv
    df_flh.at[i, 'FLH_Wind'] = wind

df_flh.to_csv('Data/flh_re.csv', index=False)