import geopandas as gpd
import numpy as np

# Daten einlesen
    #Grid
gdf_grid_morocco = gpd.read_file('Grid_morocco/grid_morocco_clear.shp')
    #Curent potential map
gdf_current_potential = gpd.read_file('grid_morocco_h2_pot_test_7.shp')
    #Rural zone
gdf_landuse_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_landuse_a_free_1.shp').to_crs("EPSG:32629")

def list_index(cell,gdf):
    intersects = gdf.intersects(cell)
    return intersects[intersects == True].index.tolist()

array_rural = np.array([])
for i in range(len(gdf_grid_morocco)):
    cell = gdf_grid_morocco.geometry[i]
    list_index_intersection = list_index(cell, gdf_landuse_utm29n)

    area = gdf_landuse_utm29n.loc[list_index_intersection].intersection(cell).area.sum()
    array_rural = np.append(array_rural, area/cell.area if area/cell.area <= 1 else 1)

array_rural -= 1
array_rural = (array_rural/array_rural.min())*100

#Replace old column with new one
weight_rural = 0.0496
gdf_current_potential['rural_zone'] = array_rural * weight_rural
gdf_current_potential['sum'] = gdf_current_potential[['avg_pv_yea','avg_windpo', 
                                                     'water aval', 'industrial',
                                                     'accessibil', 'agricultur',
                                                     'non confli', 'urban_zone',
                                                     'rural_zone']].sum(axis=1) * gdf_current_potential['nogo_zones']

gdf_current_potential.to_file('grid_morocco_h2_pot_test_7.shp', driver='ESRI Shapefile')