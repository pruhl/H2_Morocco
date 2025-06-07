import geopandas as gpd
import numpy as np

from custom import list_index

# Daten einlesen
    #Curent potential map
gdf_current_potential = gpd.read_file('grid_morocco_h2_pot_test_8.shp')
    #Agriciulture
gdf_landuse_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_landuse_a_free_1.shp').to_crs("EPSG:32629")

gdf_agriculture_morocco = gdf_landuse_utm29n[gdf_landuse_utm29n['fclass'].isin(['farmland', 'farmyard', 'meadow', 'orchard', 'vineyard'])]

array_agriculture = np.array([])
for i in range(len(gdf_current_potential)):
    cell, list_index_intersection = list_index(gdf_agriculture_morocco, i, gdf_current_potential)
    area = gdf_agriculture_morocco.loc[list_index_intersection].intersection(cell).area.sum()

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

gdf_current_potential.to_file('grid_morocco_h2_pot_test_8.shp', driver='ESRI Shapefile')