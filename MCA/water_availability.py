import geopandas as gpd
import numpy as np
import pandas as pd

# Daten einlesen
    #Grid
gdf_grid_morocco = gpd.read_file('Grid_morocco/grid_morocco_clear.shp')
    #Curent potential map
gdf_current_potential = gpd.read_file('grid_morocco_h2_pot_test_7.shp')
    #Water availability
        #Groundwater
gdf_groundwater_morocco_utm29n = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Morocco\Morocco_HG.shp").to_crs("EPSG:32629")
gdf_groundwater_western_sahara_utm29n = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Morocco\WSahara\WesternSahara_HG.shp").to_crs("EPSG:32629")
gdf_groundwater_morocco_concat = pd.concat([gdf_groundwater_morocco_utm29n, gdf_groundwater_western_sahara_utm29n.rename(columns = 
                                                                                     {'WSGLG': 'MorGLG', 'WSHGComb': 'MorHGComb'})], 
                                           ignore_index=True)
gdf_groundwater = gdf_groundwater_morocco_concat[gdf_groundwater_morocco_concat['MorHGComb'].isin(['CSIF-M/H', 'CSFK-H/VH'])]
        #Desalination plants
gdf_coast = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\morocco_coast_line.shp").to_crs("EPSG:32629")        
        #Surface Water
gdf_rivers = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\hotosm_mar_waterways_gpkg\hotosm_mar_waterways.gpkg").to_crs("EPSG:32629")

array_gw = np.array([])
for i in range(len(gdf_grid_morocco)):
    cell = gdf_grid_morocco['geometry'].iloc[i]
    cell_intersection = gdf_groundwater.intersects(cell)
    list_index_intersection = cell_intersection[cell_intersection == True].index.tolist()
    area = gdf_groundwater.loc[list_index_intersection].intersection(cell).area.sum()

    array_gw = np.append(array_gw, area/cell.area if area/cell.area <= 1 else 1)

array_gw = (array_gw/array_gw.max())*100

array_rivers = np.array([])
for i in range(len(gdf_grid_morocco)):
    cell = gdf_grid_morocco['geometry'].iloc[i]
    cell_bool_intersection = gdf_rivers.intersects(cell)
    list_index_intersection = cell_bool_intersection[cell_bool_intersection == True].index.tolist()
    rivers_length = gdf_rivers.loc[list_index_intersection].intersection(cell).length.sum()

    array_rivers = np.append(array_rivers, rivers_length)

array_rivers = (array_rivers/array_rivers.max())*100

array_desalination = np.array([])
for i in range(len(gdf_grid_morocco)):
    cell = gdf_grid_morocco['geometry'].iloc[i]
    cell_intersection = cell.intersects(gdf_coast.geometry)
    if any(cell_intersection):
        score = 100
    else:
        score = 0

    array_desalination = np.append(array_desalination, score)

array_gw = (array_gw/array_gw.max())*100

array_water = np.maximum(array_gw, array_rivers)
array_water = np.maximum(array_water, array_desalination)

#Replace old column with new one
weight_water = 0.3399
gdf_current_potential['water aval'] = array_water * weight_water
gdf_current_potential['sum'] = gdf_current_potential[['avg_pv_yea','avg_windpo', 
                                                     'water aval', 'industrial',
                                                     'accessibil', 'agricultur',
                                                     'non confli', 'urban_zone',
                                                     'rural_zone']].sum(axis=1) * gdf_current_potential['nogo_zones']

gdf_current_potential.to_file('grid_morocco_h2_pot_test_7.shp', driver='ESRI Shapefile')