import geopandas as gpd 
import numpy as np   

gdf_grid_morocco = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\Python\grid_morocco_clear.shp")
gdf_grid_morocco_centroid = gdf_grid_morocco.centroid
#Power grid
gdf_power_grid_africa = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\power_grid\africagrid20170906final.geojson")
gdf_power_grid_morocco = gdf_power_grid_africa[gdf_power_grid_africa['country'] == 'Morocco']
gdf_power_grid_morocco_utm29n = gdf_power_grid_morocco.to_crs("EPSG:32629")

#Power grid
array_distance_power_grid = np.array([])
for i in range(len(gdf_grid_morocco_centroid)):
    gdf_distance_power_grid = gdf_power_grid_morocco_utm29n['geometry'].distance(gdf_grid_morocco_centroid.iloc[i])
    distance_power_grid_min = gdf_distance_power_grid.min()
    
    array_distance_power_grid = np.append(array_distance_power_grid, distance_power_grid_min)

array_evaluation_power_grid = (array_distance_power_grid / 
                             array_distance_power_grid.max()) * 100