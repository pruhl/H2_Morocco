import geopandas as gpd
import numpy as np

from custom import list_index

# Daten einlesen
    #Curent potential map
gdf_current_potential = gpd.read_file('grid_morocco_h2_pot_test_8.shp')
    #Urban landuse
gdf_landuse_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_landuse_a_free_1.shp').to_crs("EPSG:32629")

gdf_urban_morocco = gdf_landuse_utm29n[gdf_landuse_utm29n['fclass'].isin(['residential'])]

array_urban = np.array([])
for i in range(len(gdf_current_potential)):
    cell, list_index_intersection = list_index(gdf_urban_morocco, i, gdf_current_potential)
    area = gdf_urban_morocco.loc[list_index_intersection].intersection(cell).area.sum()

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

gdf_current_potential.to_file('grid_morocco_h2_pot_test_8.shp', driver='ESRI Shapefile')