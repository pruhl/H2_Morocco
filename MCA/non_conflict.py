import geopandas as gpd
import numpy as np

# Data
    # Current potential
gdf_current_potential = gpd.read_file('Maps/mca_h2_morocco_2025.shp')
gdf_cells_centroid = gdf_current_potential.centroid
    # non_conflict
gdf_morocco = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\morocco.geojson').to_crs("EPSG:32629")
    # conflict --> Western Sahara
gdf_conflict = gpd.read_file('Data/conflict_area.shp').to_crs("EPSG:32629")

ds_distance_to_morocco = gdf_cells_centroid.distance(gdf_morocco.geometry[0])
ds_distance_to_conflict_area = gdf_cells_centroid.distance(gdf_conflict.geometry[0])
ds_ratio_distance = ds_distance_to_conflict_area/ds_distance_to_morocco
ds_ratio_distance.loc[ds_ratio_distance == 0] = 0
ds_ratio_distance.loc[ds_ratio_distance == np.inf] = 100

# Rang-skale
kriterium = (ds_ratio_distance > 0) & (ds_ratio_distance < 100) | (ds_ratio_distance > 100)

ds_ranks = ds_ratio_distance.loc[kriterium].rank().astype(int)-1
ds_ranks = (ds_ranks - 1) / (len(ds_ranks) - 1) * 100
ds_ratio_distance.loc[kriterium] = ds_ranks

ds_ratio_distance.to_csv('Data/non_conflict_areas.csv', index=False)