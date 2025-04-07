import geopandas as gpd 
import numpy as np
from shapely.geometry import point

#Data
    #Grid
gdf_grid_morocco = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\Python\grid_morocco_clear.shp")
gdf_grid_morocco_centroid = gdf_grid_morocco.centroid

    #Export Ports
gdf_export_ports = gpd.GeoDataFrame({
    'geometry': [point(-7.5, -7.5), point(35.5, 36.5)],
    'name': ['Port1', 'Port2'],
    'country': ['Morocco', 'Morocco']
    }, crs="EPSG:4326")

array_distance_export_ports = np.array([])
for i in range(len(gdf_grid_morocco_centroid)):
    cell = gdf_grid_morocco['geometry'][i]
    min_distance = gdf_export_ports['geometry'].distance(cell).min()

    array_distance_export_ports = np.append(array_distance_export_ports, min_distance)

