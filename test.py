import numpy as np
import pandas as pd
import geopandas as gpd


#Weights
dict_weights = {'avg_pv_yeald': 0.0557, 
                'avg_windpower': 0.1113, 
                'accessibility': 0.0831,
                'agricultural_land_share': 0.0194,
                'urban_zone_share': 0.0148,
                'industrial_zone_share': 0.16,
                'rural_zone_share': 0.0496,
                'water avalibility': 0.3399,
                'non conflict areas': 0.1663}

#Empty Grid
gdf_grid_morocco = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\Python\grid_morocco_clear.shp")

def list_index(cell,gdf):
    intersects = gdf.intersects(cell)
    return intersects[intersects == True].index.tolist()
#Data
    #Energy Availibility
        #PV
gdf_pv_morocco_utm29n = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Morocco_GISdata_LTAy_YearlyMonthlyTotals_GlobalSolarAtlas-v2_GEOTIFF\PV_yeald_clear.shp").to_crs("EPSG:32629")
        #Wind
gdf_wind_morocco_utm29n = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Wind_Energiedichte\wind_power_clear_150m_gross.shp").to_crs("EPSG:32629")
    #Water Availability
        #Groundwater
gdf_groundwater_morocco_utm29n = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Morocco\Morocco_HG.shp").to_crs("EPSG:32629")
gdf_groundwater_western_sahara_utm29n = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Morocco\WSahara\WesternSahara_HG.shp").to_crs("EPSG:32629")
# gdf_groundwater_western_sahara_utm29n = gdf_groundwater_western_sahara_utm29n.rename(columns = 
#                                                                                      {'WSGLG': 'MorGLG', 'WSHGComb': 'MorHGComb'})
gdf_groundwater_morocco_concat = pd.concat([gdf_groundwater_morocco_utm29n, gdf_groundwater_western_sahara_utm29n.rename(columns = 
                                                                                     {'WSGLG': 'MorGLG', 'WSHGComb': 'MorHGComb'})], 
                                           ignore_index=True)
gdf_groundwater = gdf_groundwater_morocco_concat[gdf_groundwater_morocco_concat['MorHGComb'].isin(['CSIF-M/H', 'CSFK-H/VH'])]
        #Seawater Desalination Plants

        #Surface Water
gdf_rivers = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\hotosm_mar_waterways_gpkg\hotosm_mar_waterways.gpkg").to_crs("EPSG:32629")

    #Accessibility
gdf_grid_morocco = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\Python\grid_morocco_clear.shp')

gdf_railways_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_railways_free_1.shp').to_crs("EPSG:32629")
gdf_railways_utm29n['fclass'] = 'railway'
gdf_roads_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_roads_free_1.shp').to_crs("EPSG:32629")

gdf_roads_railsways = gpd.GeoDataFrame(pd.concat([gdf_roads_utm29n, gdf_railways_utm29n], ignore_index=True), crs=gdf_roads_utm29n.crs)
classes = ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'track', 'track_grade1', 'track_grade2', 'track_grade3', 'track_grade4', 'unclassified', 'railway']
gdf_roads_railsways = gdf_roads_railsways[gdf_roads_railsways['fclass'].isin(classes)]
    #Land Availability (Agricultural Land, Urban zone, Industrial zone, Rural zone)
gdf_landuse_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_landuse_a_free_1.shp').to_crs("EPSG:32629")
gdf_agriculture_morocco = gdf_landuse_utm29n[gdf_landuse_utm29n['fclass'].isin(['farmland', 'farmyard', 'meadow', 'orchard', 'vineyard'])]
gdf_urban_morocco = gdf_landuse_utm29n[gdf_landuse_utm29n['fclass'].isin(['residential'])]
gdf_nogo_zones = gdf_landuse_utm29n[gdf_landuse_utm29n['fclass'].isin(['military', 'nature_reserve', 'recreation_ground'])]
gdf_industrie_morocco = gdf_landuse_utm29n[gdf_landuse_utm29n['fclass'].isin(['industrial'])]
    #non Conflict Areas
gdf_morocco = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\morocco.geojson').to_crs("EPSG:32629").union_all()

#Calculations
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

array_pv_yeald = np.array([])
array_wind_power = np.array([])
array_gw = np.array([])
array_rivers = np.array([])
df_accessibility = pd.DataFrame(columns = classes)
array_agriculture = np.array([])
array_urban = np.array([])
array_rural = np.array([])
array_nogo = np.array([])
array_iundustrie = np.array([])
for i in range(len(gdf_grid_morocco)):
    cell = gdf_grid_morocco.geometry[i]
    
    list_index_intersection_pv = list_index(cell, gdf_pv_morocco_utm29n)
    list_index_intersection_wind = list_index(cell, gdf_wind_morocco_utm29n)
    list_index_intersection_groundwater = list_index(cell, gdf_groundwater)
    list_index_intersection_rivers = list_index(cell, gdf_rivers)
    list_index_intersection_roads = list_index(cell, gdf_roads_railsways)
    list_index_intersection_rural = list_index(cell, gdf_landuse_utm29n)
    list_index_intersection_nogo = list_index(cell, gdf_nogo_zones)
    list_index_intersection_agriculture = list_index(cell, gdf_agriculture_morocco)
    list_index_intersection_urban = list_index(cell, gdf_urban_morocco)
    list_index_intersection_industrie = list_index(cell, gdf_industrie_morocco)

    #Energy Availibility
    if len(list_index_intersection_pv) == 0:
        pv_yeald = 0
    else:
        pv_yeald = gdf_pv_morocco_utm29n['pv_yeald'].iloc[list_index_intersection_pv].sum()/len(list_index_intersection_pv)
    
    if len(list_index_intersection_wind) == 0:
        wind_power = 0
    else:
        wind_power = gdf_wind_morocco_utm29n['wind_power'].iloc[list_index_intersection_wind].sum()/len(list_index_intersection_wind)
    
    array_pv_yeald = np.append(array_pv_yeald, pv_yeald)
    array_wind_power = np.append(array_wind_power, wind_power)
    #Water Availability
        #Groundwater
    area_gw = gdf_groundwater.loc[list_index_intersection_groundwater].intersection(cell).area.sum()
    array_gw = np.append(array_gw, area_gw/cell.area if area_gw/cell.area <= 1 else 1)
        #Rivers
    rivers_length = gdf_rivers.loc[list_index_intersection_rivers].intersection(cell).length.sum()
    array_rivers = np.append(array_rivers, rivers_length)
        #Seawater Desalination Plants
    #Accessibility
    roads_class = gdf_roads_railsways.loc[list_index_intersection_roads]['fclass']
    road_length = gdf_roads_railsways.loc[list_index_intersection_roads].intersection(cell).length

    df = pd.DataFrame({'class': roads_class, 'length': road_length})

    for y in classes:
        df_accessibility.loc[i, y] = df[df['class'] == y]['length'].sum()
    
    #Land Availability
        #Agricultural Land
    area_agri = gdf_agriculture_morocco.loc[list_index_intersection_agriculture].intersection(cell).area.sum()
    array_agriculture = np.append(array_agriculture, area_agri/cell.area)
        #Urban zone
    area_urb = gdf_urban_morocco.loc[list_index_intersection_urban].intersection(cell).area.sum()
    array_urban = np.append(array_urban, area_urb/cell.area)
        #Industrial zone
    area_ind = gdf_industrie_morocco.loc[list_index_intersection_industrie].intersection(cell).area.sum()
    array_iundustrie = np.append(array_iundustrie, area_ind/cell.area)
        #Rural zone
    area_rur = gdf_landuse_utm29n.loc[list_index_intersection_rural].intersection(cell).area.sum()
    array_rural = np.append(array_rural, area_rur/cell.area if area_rur/cell.area <= 1 else 1)
    #No Go Zones
    array_nogo = np.append(array_nogo, 0 if any(list_index_intersection_nogo) else 1)

array_evaluation_pv = (array_pv_yeald / 
                     array_pv_yeald.max()) * 100
array_evaluation_wind = (array_wind_power / 
                     array_wind_power.max()) * 100
array_gw = (array_gw/array_gw.max())*100
array_rivers = (array_rivers/array_rivers.max())*100
array_water = np.maximum(array_gw, array_rivers)

df_accessibility = (df_accessibility/df_accessibility.max())*100*weights_roads.values()
df_accessibility_sum = df_accessibility.sum(axis=1)

array_agriculture -= array_agriculture.max()
array_agriculture = (array_agriculture/array_agriculture.min())*100

array_urban -= array_urban.max()
array_urban = (array_urban/array_urban.min())*100

array_iundustrie = (array_iundustrie/array_iundustrie.max())*100

array_rural -= 1
array_rural = (array_rural/array_rural.min())*100

    #non Conflict Areas
non_conflict = gdf_grid_morocco.intersects(gdf_morocco)

non_conflict.loc[non_conflict == True] = 100
non_conflict.loc[non_conflict == False] = 0

#Sum
array_sum = (array_evaluation_pv * dict_weights['avg_pv_yeald'] + 
             array_evaluation_wind * dict_weights['avg_windpower'] + 
             array_water * dict_weights['water avalibility'] + 
             array_iundustrie * dict_weights['industrial_zone_share'] + 
             df_accessibility_sum.astype(float) * dict_weights['accessibility'] + 
             array_agriculture * dict_weights['agricultural_land_share'] + 
             non_conflict.astype(float) * dict_weights['non conflict areas']+
             array_urban * dict_weights['urban_zone_share']+
             array_rural * dict_weights['rural_zone_share'])

gdf_grid_morocco['avg_pv_yeald'] = array_evaluation_pv
gdf_grid_morocco['avg_windpower'] = array_evaluation_wind
gdf_grid_morocco['water avalibility'] = array_water
gdf_grid_morocco['industrial_zone_share'] = array_iundustrie
gdf_grid_morocco['accessibility'] = df_accessibility_sum.astype(float)
gdf_grid_morocco['agricultural_land_share'] = array_agriculture
gdf_grid_morocco['non conflict areas'] = non_conflict.astype(float)
gdf_grid_morocco['urban_zone_share'] = array_urban
gdf_grid_morocco['rural_zone_share'] = array_rural
gdf_grid_morocco['nogo_zones'] = array_nogo
gdf_grid_morocco['sum'] = array_sum * array_nogo

gdf_grid_morocco.to_file('grid_morocco_h2_pot_test_7.shp', driver='ESRI Shapefile')