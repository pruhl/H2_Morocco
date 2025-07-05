import geopandas as gpd
import numpy as np
import pandas as pd

gdf_current_potential = gpd.read_file('Maps/mca_h2_morocco_2025.shp')

gdf_coast = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\morocco_coast_line.shp").to_crs("EPSG:32629")        

# Today
df_gw_availability = pd.read_csv('Data/water_availability_gw.csv')
df_sw_availability = pd.read_csv('Data/water_availability_sw.csv')
df_water_consumption = pd.read_csv('Data/Water_Consumption.csv')

# # 2030
# df_gw_availability = pd.read_csv('Data/water_availability_gw_2030.csv')
# df_sw_availability = pd.read_csv('Data/water_availability_sw_2030.csv')
# df_water_consumption = pd.read_csv('Data/Water_Consumption_2030.csv')

# # 2050
# df_gw_availability = pd.read_csv('Data/water_availability_gw_2050.csv')
# df_sw_availability = pd.read_csv('Data/water_availability_sw_2050.csv')
# df_water_consumption = pd.read_csv('Data/Water_Consumption_2050.csv')

# # V1, Wateravailability residual
# ds_water_res = (- df_water_consumption['Water_Consumption[BCM]'] * 10**9 
#             + df_gw_availability['water_availability_gw[MCM]'] *10**6 
#             + df_sw_availability['water_availability_sw[MCM]'] *10**6)

# ds_water_res.loc[ds_water_res <= 0] = 0
# ds_water_res.loc[ds_water_res > 0] = (ds_water_res.loc[ds_water_res > 0]/
#                               ds_water_res.loc[ds_water_res > 0].max()) * 100

# array_water = np.array([])
# for i in range(len(gdf_current_potential)):
#     cell = gdf_current_potential['geometry'].iloc[i]
#     cell_intersection = cell.intersects(gdf_coast.geometry)
    
#     if any(cell_intersection):
#         score = 100
#     else:
#         score = ds_water_res[i]

#     array_water = np.append(array_water, score)

# # V2, Wateravailability
# ds_water = (df_gw_availability['water_availability_gw[MCM]'] 
#             + df_sw_availability['water_availability_sw[MCM]']) 

# ds_water.loc[ds_water <= 0] = 0
# ds_water.loc[ds_water > 0] = (ds_water.loc[ds_water > 0]/
#                               ds_water.loc[ds_water > 0].max()) * 100

# array_water = np.array([])
# for i in range(len(gdf_current_potential)):
#     cell = gdf_current_potential['geometry'].iloc[i]
#     cell_intersection = cell.intersects(gdf_coast.geometry)
    
#     if any(cell_intersection):
#         score = 100
#     else:
#         score = ds_water[i]

#     array_water = np.append(array_water, score)

# V3, 50/50 between Wateravailability and Wateravailability residual
ds_water_res = (- df_water_consumption['Water_Consumption[BCM]'] * 10**9 
            + df_gw_availability['water_availability_gw[MCM]'] *10**6 
            + df_sw_availability['water_availability_sw[MCM]'] *10**6)

ds_water = (df_gw_availability['water_availability_gw[MCM]'] 
            + df_sw_availability['water_availability_sw[MCM]'])

ds_water_res.loc[ds_water_res <= 0] = 0
ds_water_res.loc[ds_water_res > 0] = (ds_water_res.loc[ds_water_res > 0]/
                              ds_water_res.loc[ds_water_res > 0].max()) * 50

ds_water.loc[ds_water <= 0] = 0
ds_water.loc[ds_water > 0] = (ds_water.loc[ds_water > 0]/
                              ds_water.loc[ds_water > 0].max()) * 50

ds_water_50_50 = ds_water + ds_water_res

array_water = np.array([])
for i in range(len(gdf_current_potential)):
    cell = gdf_current_potential['geometry'].iloc[i]
    cell_intersection = cell.intersects(gdf_coast.geometry)
    
    if any(cell_intersection):
        score = 100
    else:
        score = ds_water_50_50[i]

    array_water = np.append(array_water, score)


#Replace old column with new one
weight_water = 0.3399
gdf_current_potential['water aval'] = array_water * weight_water
gdf_current_potential['sum'] = gdf_current_potential[['avg_pv_yea','avg_windpo', 
                                                     'water aval', 'industrial',
                                                     'accessibil', 'agricultur',
                                                     'non confli', 'urban_zone',
                                                     'rural_zone']].sum(axis=1) * gdf_current_potential['nogo_zones']
gdf_current_potential.to_file('Maps/mca_h2_morocco_2025_water_50_50.shp', driver='ESRI Shapefile')