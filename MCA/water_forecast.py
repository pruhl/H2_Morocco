import geopandas as gpd
import pandas as pd
import numpy as np

from custom import list_index

gdf_current_pot     = gpd.read_file('Maps/mca_h2_morocco_2050.shp')
gdf_precipitation   = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\Precipitation_morocco_2050_corr.shp").to_crs('EPSG:32629')
gdf_pet             = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\PET_morocco_2050_corr.shp").to_crs('EPSG:32629')
gdf_coast = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\morocco_coast_line.shp").to_crs("EPSG:32629")        
df_water_2025_sw    = pd.read_csv('Data/water_availability_sw.csv')
df_water_2025_gw    = pd.read_csv('Data/water_availability_gw.csv')
df_water_consumption_2025 = pd.read_csv('Data/Water_Consumption.csv')
df_water_consumption_2050 = pd.read_csv('Data/Water_Consumption_2050.csv')
ds_water_ges_2025        = (+ df_water_2025_gw['water_availability_gw[MCM]']  
                       + df_water_2025_sw['water_availability_sw[MCM]'])

list_geoms  = []
list_values = []
for i in range(len(gdf_precipitation)):
    for j in range(len(gdf_pet)):
        if gdf_precipitation.geometry[i].intersects(gdf_pet.geometry[j]):
            geom    = gdf_precipitation.geometry[i].intersection(gdf_pet.geometry[j])
            value   = gdf_precipitation.at[i,'Precipitat'] - gdf_pet.at[j, 'PET']
            list_values.append(value)
            list_geoms.append(geom)

gdf_cwb = gpd.GeoDataFrame(geometry=list_geoms, data={'CWB':list_values}, crs=gdf_precipitation.crs)

water_supply_2025   = ds_water_ges_2025.sum()    #MCM
water_supply_2050   = 8535                  #MCM
water_loss_2050     = water_supply_2025 - water_supply_2050 #MCM, is positiv but loss --> x MCM water of loss > 1 --> water withdrawl

list_cwb_cell       = [] 
for i in range(len(gdf_current_pot)):
    cwb_cell = 0
    for j in range(len(gdf_cwb)):
        if gdf_current_pot.geometry[i].intersects(gdf_cwb.geometry[j]):
            area_cell_in_gdf_cwb    = (gdf_current_pot.geometry[i].intersection(gdf_cwb.geometry[j])).area
            cwb_cell                += gdf_cwb.at[j,'CWB'] * area_cell_in_gdf_cwb   #Is always negativ mm*m^2
        if j == len(gdf_cwb)-1:
            list_cwb_cell.append(cwb_cell)

df_cwb_cell = pd.DataFrame(data={'CWP_zell':list_cwb_cell})
df_total_loss_water_cell = (df_cwb_cell['CWP_zell']/df_cwb_cell['CWP_zell'].sum()) * water_loss_2050    #Is positiv
df_water_cell_2050 = ds_water_ges_2025 - df_total_loss_water_cell    #Pos or neg water in each cell

# # Score for 2050
ds_water_res_2025 = (- df_water_consumption_2025['Water_Consumption[BCM]'] * 10**9 
            + df_water_2025_gw['water_availability_gw[MCM]'] *10**6 
            + df_water_2025_sw['water_availability_sw[MCM]'] *10**6)
ds_water_res_2050 = (- df_water_consumption_2050['Water_Consumption[BCM]'] * 10**9 
            + df_water_cell_2050 *10**6)

# # V1/V2 With min max in positiv values
# ds_water_res = ds_water_res_2050.copy()
# ds_water = df_water_cell_2050.copy()

# ds_water_res.loc[ds_water_res <= 0] = 0
# ds_water_res.loc[ds_water_res > 0] = (ds_water_res.loc[ds_water_res > 0]/
#                               ds_water_res_2025.max()) * 50                 #2025 as benchmark

# ds_water.loc[ds_water <= 0] = 0
# ds_water.loc[ds_water > 0] = (ds_water.loc[ds_water > 0]/
#                               ds_water_ges_2025.max()) * 50                 #2025 as benchmark

# ds_water_50_50 = ds_water + ds_water_res

# V1/V2 With/Without cost
# Cost sites are always 100
# array_water = np.array([])
# for i in range(len(gdf_current_pot)):
#     cell = gdf_current_pot.geometry[i]
#     cell_intersection = cell.intersects(gdf_coast.geometry)
    
#     if any(cell_intersection):
#         score = 100
#     else:
#         score = ds_water_50_50[i]

#     array_water = np.append(array_water, score)

# V3 Min-Max skale

ds_water        = ((df_water_cell_2050 - df_water_cell_2050.min())/
                   (ds_water_ges_2025.max()-df_water_cell_2050.min()))*50   #2025 as benchmark
ds_water_res    = ((ds_water_res_2050 - ds_water_res_2050.min())/
                   (ds_water_res_2025.max()-ds_water_res_2050.min()))*50    #2025 as benchmark

ds_water_50_50 = ds_water + ds_water_res

weight_water = 0.3399
# gdf_current_pot['water aval'] = array_water * weight_water
gdf_current_pot['water aval'] = ds_water_50_50 * weight_water
gdf_current_pot['sum'] = gdf_current_pot[['avg_pv_yea','avg_windpo', 
                                                     'water aval', 'industrial',
                                                     'accessibil', 'agricultur',
                                                     'non confli', 'urban_zone',
                                                     'rural_zone']].sum(axis=1) * gdf_current_pot['nogo_zones']
gdf_current_pot.to_file('Maps/mca_h2_morocco_2050_water_50_50_V3.shp', driver='ESRI Shapefile')