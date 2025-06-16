import geopandas as gpd
import numpy as np
import pandas as pd

gdf_current_potential = gpd.read_file('Maps/test_2.shp')

gdf_coast = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\morocco_coast_line.shp").to_crs("EPSG:32629")        

gdf_water_consumption = gpd.read_file('Data/Water_Consumption.shp')
gdf_water_exploitable = gpd.read_file('Data/water_exploitable.shp')

s_water = gdf_water_exploitable['Basin'] * 10**6 - gdf_water_consumption['Water_Cons']

s_water = s_water + (-(s_water.min()))
s_concat = (s_water / s_water.max()) * 100

array_water = np.array([])
for i in range(len(gdf_current_potential)):
    cell = gdf_current_potential['geometry'].iloc[i]
    cell_intersection = cell.intersects(gdf_coast.geometry)
    
    if any(cell_intersection):
        score = 100
    else:
        score = s_concat[i]

    array_water = np.append(array_water, score)

#Replace old column with new one
# weight_water = 0.3399   #V1
weight_water = 0.4240   #V2
gdf_current_potential['water aval'] = array_water * weight_water
gdf_current_potential['sum'] = gdf_current_potential[['avg_pv_yea','avg_windpo', 
                                                     'water aval', 'industrial',
                                                     'accessibil', 'agricultur',
                                                     'non confli', 'urban_zone',
                                                     'rural_zone']].sum(axis=1) * gdf_current_potential['nogo_zones']

gdf_current_potential.to_file('Maps/test_2.shp', driver='ESRI Shapefile')