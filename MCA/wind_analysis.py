import geopandas as gpd
import numpy as np

# Daten einlesen
    #Grid
gdf_grid_morocco = gpd.read_file('Grid_morocco/grid_morocco_clear.shp')
    #Curent potential map
gdf_current_potential = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\Python\grid_morocco_h2_pot_test_7.shx')
    #Wind
gdf_wind_morocco_utm29n = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Wind_Energiedichte\wind_power_clear_150m_gross.shp").to_crs("EPSG:32629")

def list_index(gdf, i, grid = gdf_grid_morocco):
    cell = grid['geometry'].iloc[i]
    intersects = gdf.intersects(cell)
    return cell, intersects[intersects == True].index.tolist()

array_wind_power = np.array([])
for i in range(len(gdf_grid_morocco)):
    cell_wind, list_index_intersection_wind = list_index(gdf_wind_morocco_utm29n, i)

    if len(list_index_intersection_wind) == 0:
        wind_power = 0
    else:
        wind_power = gdf_wind_morocco_utm29n['wind_power'].iloc[list_index_intersection_wind].sum()/len(list_index_intersection_wind)
    
    array_pv_yeald = np.append(array_wind_power, wind_power)

array_evaluation_wind = (array_wind_power / 
                     array_wind_power.max()) * 100

#Replace old column with new one
weight_wind = 0.1113
gdf_current_potential['avg_windpo'] = array_evaluation_wind * weight_wind
gdf_current_potential['sum'] = gdf_current_potential['avg_pv_yea','avg_windpo', 
                                                     'water aval', 'industrial',
                                                     'accessibil', 'agricultur',
                                                     'non confli', 'urban_zone',
                                                     'rural_zone' ].sum(axis=1) * gdf_current_potential['nogo_zones']

gdf_current_potential.to_file('grid_morocco_h2_pot_test_7.shp', driver='ESRI Shapefile')