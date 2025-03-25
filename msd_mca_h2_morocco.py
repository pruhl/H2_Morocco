import numpy as np
import pandas as pd
import geopandas as gpd

#Weights
dict_weights = {'avg_pv_yeald': 0.017, 
                'avg_windpower': 0.024, 
                're_projects': 0.0547,
                'h2_projects': 0.0894,
                'surface_water': 0.06,
                'groundwater': 0.02,
                'seawater_desalinationplants': 0.27,
                'distance_to_power_grid': 0.0473,
                'pipelines': 0.0334,
                'distance_to_export_ports': 0.0162,
                'accessibility': 0.0162,
                'agricultural_land_share': 0.0153,
                'urban_zone_share': 0.0123,
                'industrial_zone_share': 0.1182,
                'rural_zone_share': 0.0251,
                'population_density': 0.0413,
                'non_conflict_areas': 0.0175,
                'fundings': 0.1224}

#Empty Grid
gdf_grid_morocco = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\Python\grid_morocco_clear.shp")
gdf_grid_morocco_centroid = gdf_grid_morocco.centroid

#Data
    #Power grid
gdf_power_grid_africa = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\power_grid\africagrid20170906final.geojson")
gdf_power_grid_morocco = gdf_power_grid_africa[gdf_power_grid_africa['country'] == 'Morocco']
gdf_power_grid_morocco_utm29n = gdf_power_grid_morocco.to_crs("EPSG:32629")
    #Groundwater
gdf_groundwater_morocco = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Morocco\Morocco_HG.shp")
gdf_groundwater_morocco_utm29n = gdf_groundwater_morocco.to_crs("EPSG:32629")
gdf_groundwater_western_sahara = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Morocco\WSahara\WesternSahara_HG.shp")
gdf_groundwater_western_sahara_utm29n = gdf_groundwater_western_sahara.to_crs("EPSG:32629")
gdf_groundwater_western_sahara_utm29n = gdf_groundwater_western_sahara_utm29n.rename(columns = 
                                                                                     {'WSGLG': 'MorGLG', 'WSHGComb': 'MorHGComb'})
gdf_groundwater_morocco_concat = pd.concat([gdf_groundwater_morocco_utm29n, gdf_groundwater_western_sahara_utm29n], 
                                           ignore_index=True)
gdf_groundwater_morocco_high = pd.concat([gdf_groundwater_morocco_concat[gdf_groundwater_morocco_concat['MorHGComb'] == 'CSIF-M/H'], 
                                         gdf_groundwater_morocco_concat[gdf_groundwater_morocco_concat['MorHGComb'] == 'CSFK-H/VH']], 
                                         ignore_index=True)
    #RE-Potentials
gdf_pv_morocco = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Morocco_GISdata_LTAy_YearlyMonthlyTotals_GlobalSolarAtlas-v2_GEOTIFF\PV_yeald_clear.shp")
gdf_pv_morocco_utm29n = gdf_pv_morocco.to_crs("EPSG:32629")
# gdf_wind_morocco = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Wind_Energiedichte\wind_power_clear_150m.shp")
# gdf_wind_morocco_utm29n = gdf_wind_morocco.to_crs("EPSG:32629")
    #RE-Projects

    #H2-Projects

    #Seawater Desalination Plants

    #Surface Water

    #Pipelines

    #Export Ports

    #Accessibility

    #Landuse

    #Population Density

    #Conflict Areas

    #Fundings

#Calculations
    #Power grid
array_distance_power_grid = np.array([])
for i in range(len(gdf_grid_morocco_centroid)):
    gdf_distance_power_grid = gdf_power_grid_morocco_utm29n['geometry'].distance(gdf_grid_morocco_centroid.iloc[i])
    distance_power_grid_min = gdf_distance_power_grid.min()
    
    array_distance_power_grid = np.append(array_distance_power_grid, distance_power_grid_min)

array_evaluation_power_grid = (array_distance_power_grid / 
                             array_distance_power_grid.max()) * 100
    
    #Groundwater
gdf_union_high_water_area = gdf_groundwater_morocco_high.union_all()
gdf_intersection_area_groundwater_high = gdf_grid_morocco.intersection(gdf_union_high_water_area).area

gdf_evaluation_groundwater = (gdf_intersection_area_groundwater_high / 
                              gdf_intersection_area_groundwater_high.max()) * 100
    #RE-Potentials
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
    #RE-Projects

    #H2-Projects

    #Seawater Desalination Plants

    #Surface Water

    #Pipelines

    #Export Ports

    #Accessibility

    #Landuse

    #Population Density

    #Conflict Areas

    #Fundings

#Sum
array_sum = array_evaluation_power_grid + gdf_evaluation_groundwater + array_evaluation_pv
gdf_grid_morocco['distance'] = array_evaluation_power_grid
gdf_grid_morocco['groundwater'] = gdf_evaluation_groundwater
gdf_grid_morocco['pv_yeald'] = array_evaluation_pv
gdf_grid_morocco['sum'] = array_sum

gdf_grid_morocco.to_file('grid_morocco_h2_pot_test.shp', driver='ESRI Shapefile')