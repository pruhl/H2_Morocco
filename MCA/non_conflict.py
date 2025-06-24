import geopandas as gpd
import numpy as np

# Daten einlesen
    #Curent potential map
gdf_current_potential = gpd.read_file('Maps/grid_morocco_h2_pot_test_9.shp')
gdf_cells_centroid = gdf_current_potential.centroid
    #non_conflict
gdf_morocco = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\morocco.geojson').to_crs("EPSG:32629")#.union_all()
    #conflict
gdf_conflict = gpd.read_file('Data/conflict_area.shp').to_crs("EPSG:32629")

ds_distance_to_morocco = gdf_cells_centroid.distance(gdf_morocco.geometry[0])
ds_distance_to_conflict_area = gdf_cells_centroid.distance(gdf_conflict.geometry[0])
ds_ratio_distance = ds_distance_to_conflict_area/ds_distance_to_morocco
ds_ratio_distance.loc[ds_ratio_distance == 0] = 0
ds_ratio_distance.loc[ds_ratio_distance == np.inf] = 100

kriterium = (ds_ratio_distance > 0) & (ds_ratio_distance < 100) | (ds_ratio_distance > 100)

ds_ranks = ds_ratio_distance.loc[kriterium].rank().astype(int)-1
ds_ranks = (ds_ranks - 1) / (len(ds_ranks) - 1) * 100
ds_ratio_distance.loc[kriterium] = ds_ranks

#Replace old column with new one
weight_non_conflict = 0.1663
gdf_current_potential['non confli'] = ds_ratio_distance * weight_non_conflict
gdf_current_potential['sum'] = gdf_current_potential[['avg_pv_yea','avg_windpo', 
                                                     'water aval', 'industrial',
                                                     'accessibil', 'agricultur',
                                                     'non confli', 'urban_zone',
                                                     'rural_zone']].sum(axis=1) * gdf_current_potential['nogo_zones']

gdf_current_potential.to_file('Maps/grid_morocco_h2_pot_test_10.shp', driver='ESRI Shapefile')