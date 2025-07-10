import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

df_re_data = pd.read_csv('Data/FLH_electrolyzer.csv')

df_coordinates_pv = pd.read_excel('Data/PV_WIND_50_Punkte.xlsx', sheet_name='PV_Punkte')
df_coordinates_wind = pd.read_excel('Data/PV_WIND_50_Punkte.xlsx', sheet_name='Wind_Punkte')

df_coordinates = pd.concat([df_coordinates_pv, df_coordinates_wind], ignore_index=True)

geometry = [Point(xy) for xy in zip(df_coordinates['Longitude'], df_coordinates['Latitude'])]

gdf_re_data = gpd.GeoDataFrame(df_re_data, geometry=geometry, crs="EPSG:4326")
gdf_re_data = gdf_re_data.drop(columns= ['Unnamed: 0'])

gdf_re_data.to_file('Data/data_re_flh_electrolyzer.shp', driver='ESRI Shapefile')