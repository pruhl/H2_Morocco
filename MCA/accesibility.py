import geopandas as gpd
import pandas as pd

from custom import list_index

# Daten einlesen
    #Curent potential map
gdf_current_potential = gpd.read_file('Maps/test.shp')
    #Accessibility
gdf_railways_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_railways_free_1.shp').to_crs("EPSG:32629")
gdf_railways_utm29n['fclass'] = 'railway'
gdf_roads_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_roads_free_1.shp').to_crs("EPSG:32629")

gdf_roads_railsways = gpd.GeoDataFrame(pd.concat([gdf_roads_utm29n, gdf_railways_utm29n], ignore_index=True), crs=gdf_roads_utm29n.crs)
classes = ['motorway', 'trunk', 'primary', 'secondary', 
           'tertiary', 'track', 'track_grade1', 'track_grade2', 
           'track_grade3', 'track_grade4', 'unclassified', 'railway']
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
for i in range(len(gdf_current_potential)):
    cell_morocco, list_index_intersection = list_index(gdf_roads_railsways, i, gdf_current_potential)
    roads_class = gdf_roads_railsways.loc[list_index_intersection]['fclass']
    road_length = gdf_roads_railsways.loc[list_index_intersection].intersection(cell_morocco).length

    df = pd.DataFrame({'class': roads_class, 'length': road_length})

    for y in classes:
        a = df[df['class'] == y]['length'].sum()
        df_accessibility.loc[i, y] = a

df_accessibility = (df_accessibility/df_accessibility.max())*100*weights_roads.values()

ds_accessibility_sum = df_accessibility.sum(axis=1).astype(float)

#Replace old column with new one
# weight_accessibility = 0.0831 #V1
weight_accessibility = 0.0823   #V2
gdf_current_potential['accessibil'] = ds_accessibility_sum * weight_accessibility
gdf_current_potential['sum'] = gdf_current_potential[['avg_pv_yea','avg_windpo', 
                                                     'water aval', 'industrial',
                                                     'accessibil', 'agricultur',
                                                     'non confli', 'urban_zone',
                                                     'rural_zone']].sum(axis=1) * gdf_current_potential['nogo_zones']

gdf_current_potential.to_file('Maps/test_2.shp', driver='ESRI Shapefile')