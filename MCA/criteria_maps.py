import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as cx
import numpy as np
import matplotlib.colors as mcolors

# Data
gdf_railways_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_railways_free_1.shp').to_crs("EPSG:32629")
gdf_railways_utm29n['fclass'] = 'railway'
gdf_roads_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_roads_free_1.shp').to_crs("EPSG:32629")

gdf_roads_railsways = gpd.GeoDataFrame(pd.concat([gdf_roads_utm29n, gdf_railways_utm29n], ignore_index=True), crs=gdf_roads_utm29n.crs)

classes = ['motorway', 'trunk', 'primary', 'secondary', 
           'tertiary', 'track', 'track_grade1', 'track_grade2', 
           'track_grade3', 'track_grade4', 'unclassified', 'railway']
gdf_roads_railsways = gdf_roads_railsways[gdf_roads_railsways['fclass'].isin(classes)]


# Map MCA 2025
fig, ax = plt.subplots(figsize=(15, 10))
gdf_roads_railsways.plot(ax=ax, linewidth=0.1)
cx.add_basemap(ax, crs=gdf_roads_railsways.crs, source=cx.providers.CartoDB.Positron)
# cx.add_basemap(ax, crs=gdf_morocco_boundary.crs, source=cx.providers.OpenStreetMap.HOT)
plt.title('Accessibility', fontsize = 15)
plt.axis('off')
# plt.savefig("mca_morocco.svg", format="svg", dpi=300)
plt.show()