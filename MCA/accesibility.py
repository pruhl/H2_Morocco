import geopandas as gpd
import numpy as np
import pandas as pd

# Daten einlesen
    #Grid
gdf_grid_morocco = gpd.read_file('Grid_morocco/grid_morocco_clear.shp')
    #Curent potential map
gdf_current_potential = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\Python\grid_morocco_h2_pot_test_7.shx')
    #Accessibility
gdf_railways_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_railways_free_1.shp').to_crs("EPSG:32629")
gdf_railways_utm29n['fclass'] = 'railway'
gdf_roads_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_roads_free_1.shp').to_crs("EPSG:32629")

gdf_roads_railsways = gpd.GeoDataFrame(pd.concat([gdf_roads_utm29n, gdf_railways_utm29n], ignore_index=True), crs=gdf_roads_utm29n.crs)
classes = ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'track', 'track_grade1', 'track_grade2', 'track_grade3', 'track_grade4', 'unclassified', 'railway']
gdf_roads_railsways = gdf_roads_railsways[gdf_roads_railsways['fclass'].isin(classes)]

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
                  'unclassified':0.04, 
                  'railway':0.18}

df_accessibility = pd.DataFrame(columns = classes)
for i in range(len(gdf_grid_morocco)):
    cell_morocco = gdf_grid_morocco['geometry'].iloc[i]
    cell_bool_intersection = gdf_roads_railsways.intersects(cell_morocco)
    list_index_intersection = cell_bool_intersection[cell_bool_intersection == True].index.tolist()
    roads_class = gdf_roads_railsways.loc[list_index_intersection]['fclass']
    road_length = gdf_roads_railsways.loc[list_index_intersection].intersection(cell_morocco).length

    df = pd.DataFrame({'class': roads_class, 'length': road_length})

    for y in classes:
        a = df[df['class'] == y]['length'].sum()
        df_accessibility.loc[i, y] = a

df_accessibility = (df_accessibility/df_accessibility.max())*100*weights_roads.values()

ds_accessibility_sum = df_accessibility.sum(axis=1).astype(float)

#Replace old column with new one
gdf_current_potential['accessibil'] = ds_accessibility_sum

gdf_current_potential.to_file('grid_morocco_h2_pot_test_7.shp', driver='ESRI Shapefile')