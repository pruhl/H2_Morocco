import geopandas as gpd
import numpy as np

# Daten einlesen
    #Curent potential map
gdf_current_potential = gpd.read_file('grid_morocco_h2_pot_test_8.shp')
    #No-Go Zones
#Military, nature reserves, recreation grounds
gdf_landuse_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_landuse_a_free_1.shp').to_crs("EPSG:32629")

gdf_nogo_zones = gdf_landuse_utm29n[gdf_landuse_utm29n['fclass'].isin(['military', 'nature_reserve', 'recreation_ground'])]
gdf_nogo_zones.reset_index(drop=True, inplace=True)
gdf_nogo_zones.index = range(len(gdf_nogo_zones))

#topografic
gdf_topo_utm29n = gpd.read_file('ToPo_1500.shp').to_crs("EPSG:32629")

array_nogo = np.array([])
for i in range(len(gdf_current_potential)):
    cell = gdf_current_potential['geometry'].iloc[i]
    cell_intersection = gdf_nogo_zones.intersects(cell)
    list_index_intersection = cell_intersection[cell_intersection == True].index.tolist()

    if len(list_index_intersection) == 0:
        a = 1
    else:
        intersected_area = gdf_nogo_zones.iloc[list_index_intersection].intersection(cell).area.sum()
        if intersected_area/cell.area >= 0.5:
            a = 0
        else:
            a = 1

    array_nogo = np.append(array_nogo, a)

#Replace old column with new one
gdf_current_potential['nogo_zones'] = np.minimum(array_nogo, gdf_topo_utm29n['NoGos'])
gdf_current_potential['sum'] = gdf_current_potential[['avg_pv_yea','avg_windpo', 
                                                     'water aval', 'industrial',
                                                     'accessibil', 'agricultur',
                                                     'non confli', 'urban_zone',
                                                     'rural_zone']].sum(axis=1) * gdf_current_potential['nogo_zones']

gdf_current_potential.to_file('grid_morocco_h2_pot_test_8.shp', driver='ESRI Shapefile')