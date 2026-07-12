import geopandas as gpd
import numpy as np

# Data
    # Current potential
gdf_grid = gpd.read_file('Grid_morocco/grid_morocco_clear.shp')
gdf_cells_centroid = gdf_grid.centroid
    # non_conflict
gdf_morocco = gpd.read_file('Data\morocco.geojson').to_crs("EPSG:32629")
    # conflict --> Western Sahara

ds_distance_to_morocco = gdf_cells_centroid.distance(gdf_morocco.geometry.iloc[0])

ds_ratio_distance = ds_distance_to_morocco/ds_distance_to_morocco.max() * 100

# Rang-skale
kriterium = (ds_ratio_distance > 0) & (ds_ratio_distance < 100) | (ds_ratio_distance > 100)

ds_ranks = ds_ratio_distance.loc[kriterium].rank().astype(int)-1
ds_ranks = (ds_ranks - 1) / (len(ds_ranks) - 1) * 100
ds_ratio_distance.loc[kriterium] = ds_ranks

ds_ratio_distance.to_csv('results/results_non_conflict_areas.csv', index=False)

# Map non-conflict areas
gdf_grid['non_conflict'] = ds_ratio_distance
gdf_grid.plot(column='non_conflict', cmap='YlGnBu', legend=False)