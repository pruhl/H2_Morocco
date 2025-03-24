import numpy as np
import pandas as pd
import geopandas as gpd


#Einlesen des Grundrasters
gdf_grid_morocco = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\Python\grid_morocco_clear.shp")
gdf_grid_morocco_centroid = gdf_grid_morocco.centroid
#gdf_raster_morocco.plot()

# Stromnetz
gdf_power_grid_africa = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\power_grid\africagrid20170906final.geojson")
gdf_power_grid_morocco = gdf_power_grid_africa[gdf_power_grid_africa['country'] == 'Morocco']
gdf_power_grid_morocco_utm29n = gdf_power_grid_morocco.to_crs("EPSG:32629")
#gdf_grid_morocco_utm29n.plot()

# Grundwasserpotenzial
gdf_groundwater_morocco = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Morocco\Morocco_HG.shp")
gdf_groundwater_morocco_utm29n = gdf_groundwater_morocco.to_crs("EPSG:32629")
gdf_groundwater_western_sahara = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Morocco\WSahara\WesternSahara_HG.shp")
gdf_groundwater_western_sahara_utm29n = gdf_groundwater_western_sahara.to_crs("EPSG:32629")
gdf_groundwater_western_sahara_utm29n = gdf_groundwater_western_sahara_utm29n.rename(columns = 
                                                                                     {'WSGLG': 'MorGLG', 'WSHGComb': 'MorHGComb'})
gdf_groundwater_morocco_concat = pd.concat([gdf_groundwater_morocco_utm29n, gdf_groundwater_western_sahara_utm29n], 
                                           ignore_index=True)
gdf_groundwater_morocco_high = pd.concat([gdf_groundwater_morocco_concat[gdf_groundwater_morocco_concat['MorHGComb'] == 'CSIF-M/H'], 
                                         gdf_groundwater_morocco_concat[gdf_groundwater_morocco_concat['MorHGComb'] == 'CSFK-H/VH']], 
                                         ignore_index=True)

# EE-Potenziale
gdf_pv_morocco = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Morocco_GISdata_LTAy_YearlyMonthlyTotals_GlobalSolarAtlas-v2_GEOTIFF\PV_yeald_clear.shp")
gdf_pv_morocco_utm29n = gdf_pv_morocco.to_crs("EPSG:32629")
# gdf_wind_morocco = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Wind_Energiedichte\wind_power_clear_150m.shp")

# Vergleichsoperationen
# Stromnetz
distance_array = np.array([])
indicators_array = np.array([])
for i in range(len(gdf_grid_morocco_centroid)):
    distance = gdf_power_grid_morocco_utm29n['geometry'].distance(gdf_grid_morocco_centroid.iloc[i])
    distance_min = distance.min()
    if distance_min < 100000:
        indicator_distance = 1/3
    else:
       indicator_distance = 0
    
    distance_array = np.append(distance_array, distance_min)
    indicators_array = np.append(indicators_array, indicator_distance)

# Grundwasser
union = gdf_groundwater_morocco_high.union_all()
intersection_area = gdf_grid_morocco.intersection(union).area
indicator_groundwater_array = np.array([])
for i in range(len(gdf_grid_morocco)):
    if intersection_area[i] < 50000000:
        indicator_groundwater = 0
    else:
        indicator_groundwater = 1/3

    indicator_groundwater_array = np.append(indicator_groundwater_array, indicator_groundwater)

# PV
indicator_pv_array = np.array([])
pv_yeald_array = np.array([])
for i in range(len(gdf_grid_morocco)):
    cell = gdf_grid_morocco['geometry'].iloc[i]
    cell_intersection = gdf_pv_morocco_utm29n.intersects(cell)
    list_index_intersection = cell_intersection[cell_intersection == True].index.tolist()
    if len(list_index_intersection) == 0:
        pv_yeald = 0
    else:
        pv_yeald = gdf_pv_morocco_utm29n['pv_yeald'].iloc[list_index_intersection].sum()/len(list_index_intersection)
    if pv_yeald < 1500:
        indicator_pv = 0
    else:
        indicator_pv = 1/3
    
    pv_yeald_array = np.append(pv_yeald_array, pv_yeald)
    indicator_pv_array = np.append(indicator_pv_array, indicator_pv)

# if cell_intersection == True:

sum_array = indicators_array + indicator_groundwater_array + indicator_pv_array
gdf_grid_morocco['distance'] = distance_array
gdf_grid_morocco['distance_indicator'] = indicators_array 
gdf_grid_morocco['groundwater_indicator'] = indicator_groundwater_array
gdf_grid_morocco['pv_indicator'] = indicator_pv_array
gdf_grid_morocco['pv_yeald'] = pv_yeald_array
gdf_grid_morocco['sum'] = sum_array

gdf_grid_morocco.to_file('grid_morocco_h2_pot.shp', driver='ESRI Shapefile')