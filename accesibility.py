import geopandas as gpd
import numpy as np
import pandas as pd

# Daten einlesen
gdf_grid_morocco = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\Python\grid_morocco_clear.shp')

gdf_roads_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_roads_free_1.shp').to_crs("EPSG:32629")
classes = ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'track', 'track_grade1', 'track_grade2', 'track_grade3', 'track_grade4', 'unclassified']
weights_roads = {'motorway': 0.25,
                  'trunk': 0.18,
                  'primary':0.12, 
                  'secondary':0.09, 
                  'tertiary':0.06, 
                  'track':0.01, 
                  'track_grade1':0.03, 
                  'track_grade2':0.02, 
                  'track_grade3':0.01, 
                  'track_grade4':0.01, 
                  'unclassified':0.04}
gdf_roads_utm29n = gdf_roads_utm29n[gdf_roads_utm29n['fclass'].isin(classes)]

df_sum = pd.DataFrame(columns = classes)
for i in range(len(gdf_grid_morocco)):
    cell_morocco = gdf_grid_morocco['geometry'].iloc[i]
    cell_bool_intersection = gdf_roads_utm29n.intersects(cell_morocco)
    list_index_intersection_roads = cell_bool_intersection[cell_bool_intersection == True].index.tolist()
    roads_class = gdf_roads_utm29n.loc[list_index_intersection_roads]['fclass']
    road_length = gdf_roads_utm29n.loc[list_index_intersection_roads].intersection(cell_morocco).length

    df = pd.DataFrame({'class': roads_class, 'length': road_length})

    for y in classes:
        a = df[df['class'] == y]['length'].sum()
        df_sum.loc[i, y] = a

df_sum = (df_sum/df_sum.max())*100*weights_roads.values()

df_sum_cells = df_sum.sum(axis=1)

# gdf_grid_morocco.to_file('industrial_share.shp', driver='ESRI Shapefile')