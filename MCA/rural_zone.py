import pandas as pd
import geopandas as gpd
import numpy as np

from custom import list_index

# Data
    # Current potential
gdf_current_potential = gpd.read_file('Maps/mca_h2_morocco_2050.shp')
    # Rural zone
    # Source: FAO, via: https://data.apps.fao.org/catalog/dataset/fad3f475-8973-463f-b56a-e6b6535c1db5  --> Morocco
    # Source: FAO, via: https://data.apps.fao.org/catalog/iso/75aaf5c5-d579-425a-97fb-aa4580536df2      --> Western Sahara

gdf_landuse_mar         = gpd.read_file(r'C:\Users\psclr\Downloads\geonetwork_landcover_mar_gc_adg\mar_gc_adg.shp').to_crs("EPSG:32629") 
gdf_landuse_wsa         = gpd.read_file(r'C:\Users\psclr\Downloads\geonetwork_landcover_wsa_gc_adg\wsa_gc_adg.shp').to_crs("EPSG:32629")
gdf_landuse_concat      = gpd.GeoDataFrame(pd.concat([gdf_landuse_mar, gdf_landuse_wsa]))       #Today

    # Same source, but for future landuse (from forecast_landuse.py)
# gdf_landuse_concat      = gpd.read_file('Data/morocco_landuse_2050.shp')    #Landuse 2050

gdf_landuse_rural       = gdf_landuse_concat[gdf_landuse_concat['GRIDCODE'].isin([200, 201, 202, 203, 220, 230, 
                                                                                  40, 41,42,50,60,70,90,91,92,
                                                                                  100,101,110,120,130,131,134,
                                                                                  140,141,150,151,152,160,161,
                                                                                  162,170,180,181,185])]

array_rural = np.array([])
for i in range(len(gdf_current_potential)):
    cell, list_index_intersection = list_index(gdf_landuse_rural, i, gdf_current_potential)

    area = gdf_landuse_rural.loc[list_index_intersection].intersection(cell).area.sum()
    array_rural = np.append(array_rural, area/cell.area)

df_rural = pd.DataFrame(data = array_rural)

df_rural.to_csv('Data/results_rural.csv', index=False)