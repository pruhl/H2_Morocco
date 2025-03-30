import geopandas as gpd
import numpy as np
import pandas as pd

# Daten einlesen
gdf_grid_morocco = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\Python\grid_morocco_clear.shp')

gdf_landuse_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_landuse_a_free_1.shp').to_crs("EPSG:32629")

gdf_industrie_morocco = gdf_landuse_utm29n[gdf_landuse_utm29n['fclass'].isin(['industrial'])].union_all()

gdf_intersection_industrie = (gdf_grid_morocco.intersection(gdf_industrie_morocco).area/gdf_grid_morocco.area)*100

gdf_grid_morocco['indust'] = gdf_intersection_industrie

# gdf_grid_morocco.to_file('industrial_share.shp', driver='ESRI Shapefile')