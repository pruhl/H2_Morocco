import geopandas as gpd
import numpy as np
import pandas as pd

df = pd.read_csv('Opt_FLH/FLH_electrolyzer.csv', index_col=0)
df.reset_index(drop=True, inplace=True)
df_1 = pd.read_csv('Opt_FLH/pv_wind_electricity.csv', index_col=0).sum()

df_pv = df_1.iloc[::2]
df_wind = df_1.iloc[1::2]
df_wind.reset_index(drop=True, inplace=True)

#df['FLH_electrolyzer'].plot(use_index=False, secondary_y=df_wind)

df_concat = pd.concat([df_wind, df], axis=1)
df_concat.reset_index(drop=True, inplace=True)
df_concat.sort_values(by = 0)