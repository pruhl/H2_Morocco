import pandas as pd
import geopandas as gpd
import numpy as np

from custom import list_index

# Data
    # Current potential, from previous MCA
gdf_current_potential = gpd.read_file('Maps/mca_h2_morocco_2050.shp')

    # Agriculture
    # Source: FAO, via: https://data.apps.fao.org/catalog/dataset/fad3f475-8973-463f-b56a-e6b6535c1db5  --> Morocco
    # Source: FAO, via: https://data.apps.fao.org/catalog/iso/75aaf5c5-d579-425a-97fb-aa4580536df2      --> Western Sahara

gdf_landuse_mar         = gpd.read_file(r'C:\Users\psclr\Downloads\geonetwork_landcover_mar_gc_adg\mar_gc_adg.shp').to_crs("EPSG:32629") 
gdf_landuse_wsa         = gpd.read_file(r'C:\Users\psclr\Downloads\geonetwork_landcover_wsa_gc_adg\wsa_gc_adg.shp').to_crs("EPSG:32629")
gdf_landuse_concat      = gpd.GeoDataFrame(pd.concat([gdf_landuse_mar, gdf_landuse_wsa])) #Today

    # Same source, but for future landuse (from forecast_landuse.py)
# gdf_landuse_concat      = gpd.read_file('Data/morocco_landuse_2050.shp')    #Landuse 2050

gdf_landuse_agri        = gdf_landuse_concat[gdf_landuse_concat['GRIDCODE'].isin([11, 12, 13, 14, 15, 16, 20, 21, 30, 31, 32])]

array_agriculture = np.array([])
for i in range(len(gdf_current_potential)):
    cell, list_index_intersection = list_index(gdf_landuse_agri, i, gdf_current_potential)
    area = gdf_landuse_agri.loc[list_index_intersection].intersection(cell).area.sum()

    array_agriculture = np.append(array_agriculture, area/cell.area)

array_agriculture -= array_agriculture.max()
array_agriculture = (array_agriculture/array_agriculture.min())*100

#Replace old column with new one
weight_agri = 0.0194
gdf_current_potential['agricultur'] = array_agriculture * weight_agri
gdf_current_potential['sum'] = gdf_current_potential[['avg_pv_yea','avg_windpo', 
                                                     'water aval', 'industrial',
                                                     'accessibil', 'agricultur',
                                                     'non confli', 'urban_zone',
                                                     'rural_zone']].sum(axis=1) * gdf_current_potential['nogo_zones']

gdf_current_potential.to_file('Maps/mca_h2_morocco_2050.shp', driver='ESRI Shapefile')