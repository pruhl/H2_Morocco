import pandas as pd
import geopandas as gpd
import numpy as np

from custom import list_index

# Data
    # Current potential
gdf_current_potential = gpd.read_file('Maps/mca_h2_morocco_2050.shp')
    # Urban landuse
    # Source: FAO, via: https://data.apps.fao.org/catalog/dataset/fad3f475-8973-463f-b56a-e6b6535c1db5  --> Morocco
    # Source: FAO, via: https://data.apps.fao.org/catalog/iso/75aaf5c5-d579-425a-97fb-aa4580536df2      --> Western Sahara

gdf_landuse_mar         = gpd.read_file(r'C:\Users\psclr\Downloads\geonetwork_landcover_mar_gc_adg\mar_gc_adg.shp').to_crs("EPSG:32629") 
gdf_landuse_wsa         = gpd.read_file(r'C:\Users\psclr\Downloads\geonetwork_landcover_wsa_gc_adg\wsa_gc_adg.shp').to_crs("EPSG:32629")
gdf_landuse_concat      = gpd.GeoDataFrame(pd.concat([gdf_landuse_mar, gdf_landuse_wsa]))   #Today

    # Same source, but for future landuse (from forecast_landuse.py)
# gdf_landuse_concat      = gpd.read_file('Data/morocco_landuse_2050.shp')    #Landuse 2050

gdf_landuse_urban       = gdf_landuse_concat[gdf_landuse_concat['GRIDCODE'].isin([190])]

array_urban = np.array([])
for i in range(len(gdf_current_potential)):
    cell, list_index_intersection = list_index(gdf_landuse_urban, i, gdf_current_potential)
    area = gdf_landuse_urban.loc[list_index_intersection].intersection(cell).area.sum()

    array_urban = np.append(array_urban, area/cell.area)

df_urban = pd.DataFrame(data = array_urban)

df_urban.to_csv('Data/results_urban.csv', index=False)