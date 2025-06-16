import geopandas as gpd
import numpy as np

from custom import list_index

# Daten einlesen
    #Curent potential map
gdf_current_potential = gpd.read_file('Maps/test_2.shp')
    #Wind
gdf_wind_morocco_utm29n = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Wind_Energiedichte\wind_yeald\Wind_pot_morocco_FLH.shp").to_crs("EPSG:32629")

array_wind_power = np.array([])
for i in range(len(gdf_current_potential)):
    cell_wind, list_index_intersection_wind = list_index(gdf_wind_morocco_utm29n, i, gdf_current_potential)

    if len(list_index_intersection_wind) == 0:
        wind_power = 0
    else:
        wind_power = gdf_wind_morocco_utm29n['FLH_wind'].iloc[list_index_intersection_wind].sum()/len(list_index_intersection_wind)
    
    array_wind_power = np.append(array_wind_power, wind_power)

array_evaluation_wind = (array_wind_power / 
                     array_wind_power.max()) * 100

#Replace old column with new one
# weight_wind = 0.1113    #V1
weight_wind = 0.1315    #V2
gdf_current_potential['avg_windpo'] = array_evaluation_wind * weight_wind
gdf_current_potential['sum'] = gdf_current_potential[['avg_pv_yea','avg_windpo', 
                                                     'water aval', 'industrial',
                                                     'accessibil', 'agricultur',
                                                     'non confli', 'urban_zone',
                                                     'rural_zone']].sum(axis=1) * gdf_current_potential['nogo_zones']

gdf_current_potential.to_file('Maps/test_2.shp', driver='ESRI Shapefile')