import geopandas as gpd
import numpy as np
import pandas as pd

from custom import list_index

# Data
    # Current potential
gdf_current_potential = gpd.read_file('Maps/mca_h2_morocco_2025.shp')
    # Wind
    # Sorce: Global Wind Atlas
gdf_wind_morocco_utm29n = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Wind_Energiedichte\wind_yeald\Wind_pot_morocco_FLH.shp").to_crs("EPSG:32629")

array_wind_power = np.array([])
for i in range(len(gdf_current_potential)):
    cell_wind, list_index_intersection_wind = list_index(gdf_wind_morocco_utm29n, i, gdf_current_potential)

    if len(list_index_intersection_wind) == 0:
        wind_power = 0
    else:
        wind_power = gdf_wind_morocco_utm29n['FLH_wind'].iloc[list_index_intersection_wind].sum()/len(list_index_intersection_wind)
    
    array_wind_power = np.append(array_wind_power, wind_power)

df_wind_flh = pd.DataFrame(data = array_wind_power)

df_wind_flh.to_csv('Data/results_wind_flh.csv', index=False)