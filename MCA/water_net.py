import geopandas as gpd
import numpy as np
import pandas as pd

gdf_current_potential = gpd.read_file('Maps/mca_h2_morocco_2025.shp')

gdf_coast = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\morocco_coast_line.shp").to_crs("EPSG:32629")        

# Today
df_gw_availability = pd.read_csv('Data/water_availability_gw.csv')
df_sw_availability = pd.read_csv('Data/water_availability_sw.csv')
df_water_consumption = pd.read_csv('Data/Water_Consumption.csv')

# 50/50 between Wateravailability and Wateravailability residual
ds_water_res = (- df_water_consumption['Water_Consumption[BCM]'] * 10**9 
            + df_gw_availability['water_availability_gw[MCM]'] *10**6 
            + df_sw_availability['water_availability_sw[MCM]'] *10**6)

ds_water = (df_gw_availability['water_availability_gw[MCM]'] 
            + df_sw_availability['water_availability_sw[MCM]'])

    # Cost = 100, negativ values = 0, positiv values min-max scale
ds_water_res.loc[ds_water_res <= 0] = 0
ds_water_res.loc[ds_water_res > 0] = (ds_water_res.loc[ds_water_res > 0]/
                              ds_water_res.loc[ds_water_res > 0].max()) * 50

ds_water = (ds_water/
            ds_water.max()) * 50

ds_water_50_50 = ds_water + ds_water_res

     # Check if cell is at coast, if yes give score 100
array_water = np.array([])
for i in range(len(gdf_current_potential)):
    cell = gdf_current_potential.geometry[i]
    cell_intersection = cell.intersects(gdf_coast.geometry)
    
    if any(cell_intersection):
        score = 100
    else:
        score = ds_water_50_50[i]

    array_water = np.append(array_water, score)

df_water = pd.DataFrame(data = array_water)

df_water.to_csv('Data/results_water_res_availabil.csv', index=False)