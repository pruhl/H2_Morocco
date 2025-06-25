import pandas as pd
import geopandas as gpd
import numpy as np

from custom import list_index

# Data
    #Curent potential
gdf_current_potential = gpd.read_file('Maps/mca_h2_morocco_2050.shp')
    #Rural zone
# gdf_landuse_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_landuse_a_free_1.shp').to_crs("EPSG:32629")
# gdf_landuse_mar         = gpd.read_file(r'C:\Users\psclr\Downloads\geonetwork_landcover_mar_gc_adg\mar_gc_adg.shp').to_crs("EPSG:32629") 

# gdf_landuse_wsa         = gpd.read_file(r'C:\Users\psclr\Downloads\geonetwork_landcover_wsa_gc_adg\wsa_gc_adg.shp').to_crs("EPSG:32629")

# gdf_landuse_concat      = gpd.GeoDataFrame(pd.concat([gdf_landuse_mar, gdf_landuse_wsa]))       #Today

# gdf_landuse_concat      = gpd.read_file('Data/morocco_landuse_2030.shp')    #Landuse 2030
gdf_landuse_concat      = gpd.read_file('Data/morocco_landuse_2050.shp')    #Landuse 2050

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

array_rural = (array_rural/array_rural.max())*100

#Replace old column with new one
weight_rural = 0.0496
gdf_current_potential['rural_zone'] = array_rural * weight_rural
gdf_current_potential['sum'] = gdf_current_potential[['avg_pv_yea','avg_windpo', 
                                                     'water aval', 'industrial',
                                                     'accessibil', 'agricultur',
                                                     'non confli', 'urban_zone',
                                                     'rural_zone']].sum(axis=1) * gdf_current_potential['nogo_zones']

gdf_current_potential.to_file('Maps/mca_h2_morocco_2050.shp', driver='ESRI Shapefile')