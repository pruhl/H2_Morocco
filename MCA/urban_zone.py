import pandas as pd
import geopandas as gpd
import numpy as np

from custom import list_index

# Data
    #Curent potential
gdf_current_potential = gpd.read_file('Maps/mca_h2_morocco_2050.shp')
    #Urban landuse
# gdf_landuse_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_landuse_a_free_1.shp').to_crs("EPSG:32629")
# gdf_urban_morocco = gdf_landuse_utm29n[gdf_landuse_utm29n['fclass'].isin(['residential'])]

# gdf_landuse_mar         = gpd.read_file(r'C:\Users\psclr\Downloads\geonetwork_landcover_mar_gc_adg\mar_gc_adg.shp').to_crs("EPSG:32629") 

# gdf_landuse_wsa         = gpd.read_file(r'C:\Users\psclr\Downloads\geonetwork_landcover_wsa_gc_adg\wsa_gc_adg.shp').to_crs("EPSG:32629")

# gdf_landuse_concat      = gpd.GeoDataFrame(pd.concat([gdf_landuse_mar, gdf_landuse_wsa]))   #Today

# gdf_landuse_concat      = gpd.read_file('Data/morocco_landuse_2030.shp')    #Landuse 2030
gdf_landuse_concat      = gpd.read_file('Data/morocco_landuse_2050.shp')    #Landuse 2050

gdf_landuse_urban       = gdf_landuse_concat[gdf_landuse_concat['GRIDCODE'].isin([190])]

array_urban = np.array([])
for i in range(len(gdf_current_potential)):
    cell, list_index_intersection = list_index(gdf_landuse_urban, i, gdf_current_potential)
    area = gdf_landuse_urban.loc[list_index_intersection].intersection(cell).area.sum()

    array_urban = np.append(array_urban, area/cell.area)

array_urban -= array_urban.max()
array_urban = (array_urban/array_urban.min())*100

#Replace old column with new one
weight_urban = 0.0148
gdf_current_potential['urban_zone'] = array_urban * weight_urban
gdf_current_potential['sum'] = gdf_current_potential[['avg_pv_yea','avg_windpo', 
                                                     'water aval', 'industrial',
                                                     'accessibil', 'agricultur',
                                                     'non confli', 'urban_zone',
                                                     'rural_zone']].sum(axis=1) * gdf_current_potential['nogo_zones']

gdf_current_potential.to_file('Maps/mca_h2_morocco_2050.shp', driver='ESRI Shapefile')