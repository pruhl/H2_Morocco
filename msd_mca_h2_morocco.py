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
                'non_conflict_areas': 0.1663}

#Empty Grid
gdf_grid_morocco = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\Python\grid_morocco_clear.shp")
gdf_grid_morocco_centroid = gdf_grid_morocco.centroid

#Data
    #Energy Availibility
        #PV
gdf_pv_morocco = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Morocco_GISdata_LTAy_YearlyMonthlyTotals_GlobalSolarAtlas-v2_GEOTIFF\PV_yeald_clear.shp")
gdf_pv_morocco_utm29n = gdf_pv_morocco.to_crs("EPSG:32629")
        #Wind
gdf_wind_morocco = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Wind_Energiedichte\wind_power_clear_150m.shp")
gdf_wind_morocco_utm29n = gdf_wind_morocco.to_crs("EPSG:32629")
    #Water Availability
        #Groundwater
gdf_groundwater_morocco_utm29n = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Morocco\Morocco_HG.shp").to_crs("EPSG:32629")
gdf_groundwater_western_sahara_utm29n = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Morocco\WSahara\WesternSahara_HG.shp").to_crs("EPSG:32629")
gdf_groundwater_western_sahara_utm29n = gdf_groundwater_western_sahara_utm29n.rename(columns = 
                                                                                     {'WSGLG': 'MorGLG', 'WSHGComb': 'MorHGComb'})
gdf_groundwater_morocco_concat = pd.concat([gdf_groundwater_morocco_utm29n, gdf_groundwater_western_sahara_utm29n], 
                                           ignore_index=True)
gdf_groundwater_morocco_high = pd.concat([gdf_groundwater_morocco_concat[gdf_groundwater_morocco_concat['MorHGComb'] == 'CSIF-M/H'], 
                                         gdf_groundwater_morocco_concat[gdf_groundwater_morocco_concat['MorHGComb'] == 'CSFK-H/VH']], 
                                         ignore_index=True)
        #Seawater Desalination Plants

        #Surface Water

    #Accessibility

    #Land Availability (Agricultural Land, Urban zone, Industrial zone, Rural zone)
gdf_landuse_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_landuse_a_free_1.shp').to_crs("EPSG:32629")

    #Conflict Areas

#Calculations
    #Energy Availibility
        #PV
array_pv_yeald = np.array([])
for i in range(len(gdf_grid_morocco)):
    cell_morocco = gdf_grid_morocco['geometry'].iloc[i]
    cell_intersection = gdf_pv_morocco_utm29n.intersects(cell_morocco)
    list_index_intersection = cell_intersection[cell_intersection == True].index.tolist()
    if len(list_index_intersection) == 0:
        pv_yeald = 0
    else:
        pv_yeald = gdf_pv_morocco_utm29n['pv_yeald'].iloc[list_index_intersection].sum()/len(list_index_intersection)
    
    array_pv_yeald = np.append(array_pv_yeald, pv_yeald)

array_evaluation_pv = (array_pv_yeald / 
                     array_pv_yeald.max()) * 100
        #Wind        
    #Water Availability
        #Groundwater
gdf_union_high_water_area = gdf_groundwater_morocco_high.union_all()
gdf_intersection_area_groundwater_high = gdf_grid_morocco.intersection(gdf_union_high_water_area).area

gdf_evaluation_groundwater = (gdf_intersection_area_groundwater_high / 
                              gdf_intersection_area_groundwater_high.max()) * 100
        #Seawater Desalination Plants

        #Surface Water

    #Accessibility

    #Land Availability
        #Agricultural Land

        #Urban zone

        #Industrial zone
gdf_industrie_morocco = gdf_landuse_utm29n[gdf_landuse_utm29n['fclass'].isin(['industrial'])].union_all()

gdf_intersection_industrie = (gdf_grid_morocco.intersection(gdf_industrie_morocco).area/gdf_grid_morocco.area)*100
        #Rural zone

    #Conflict Areas

#Sum
array_sum = gdf_evaluation_groundwater + array_evaluation_pv + gdf_intersection_industrie
gdf_grid_morocco['pv_yeald'] = array_evaluation_pv
gdf_grid_morocco['groundwater'] = gdf_evaluation_groundwater
gdf_grid_morocco['indust'] = gdf_intersection_industrie
gdf_grid_morocco['sum'] = array_sum


gdf_grid_morocco.to_file('grid_morocco_h2_pot_test.shp', driver='ESRI Shapefile')