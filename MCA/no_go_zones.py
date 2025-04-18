import geopandas as gpd
import numpy as np

# Daten einlesen
    #Grid
gdf_grid_morocco = gpd.read_file('Grid_morocco/grid_morocco_clear.shp')
    #Curent potential map
gdf_current_potential = gpd.read_file('grid_morocco_h2_pot_test_7.shp')
    #No-Go Zones
gdf_landuse_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_landuse_a_free_1.shp').to_crs("EPSG:32629")

gdf_nogo_zones = gdf_landuse_utm29n[gdf_landuse_utm29n['fclass'].isin(['military', 'nature_reserve', 'recreation_ground'])]

array_nogo = np.array([])
for i in range(len(gdf_grid_morocco)):
    cell = gdf_grid_morocco['geometry'].iloc[i]
    cell_intersection = gdf_nogo_zones.intersects(cell)
    list_index_intersection = cell_intersection[cell_intersection == True].index.tolist()

    array_nogo = np.append(array_nogo, 0 if any(list_index_intersection) else 1)

#Replace old column with new one
gdf_current_potential['nogo_zones'] = array_nogo
gdf_current_potential['sum'] = gdf_current_potential[['avg_pv_yea','avg_windpo', 
                                                     'water aval', 'industrial',
                                                     'accessibil', 'agricultur',
                                                     'non confli', 'urban_zone',
                                                     'rural_zone']].sum(axis=1) * gdf_current_potential['nogo_zones']

gdf_current_potential.to_file('grid_morocco_h2_pot_test_7.shp', driver='ESRI Shapefile')