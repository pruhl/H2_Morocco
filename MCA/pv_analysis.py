import geopandas as gpd
import numpy as np

# Daten einlesen
    #Grid
gdf_grid_morocco = gpd.read_file('Grid_morocco/grid_morocco_clear.shp')
    #Curent potential map
gdf_current_potential = gpd.read_file('grid_morocco_h2_pot_test_7.shp')
    #PV
gdf_pv_morocco_utm29n = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Morocco_GISdata_LTAy_YearlyMonthlyTotals_GlobalSolarAtlas-v2_GEOTIFF\PV_yeald_clear.shp").to_crs("EPSG:32629")

def list_index(gdf, i, grid = gdf_grid_morocco):
    cell = grid['geometry'].iloc[i]
    intersects = gdf.intersects(cell)
    return cell, intersects[intersects == True].index.tolist()

array_pv_yeald = np.array([])
for i in range(len(gdf_grid_morocco)):
    cell_pv, list_index_intersection_pv = list_index(gdf_pv_morocco_utm29n, i)

    if len(list_index_intersection_pv) == 0:
        pv_yeald = 0
    else:
        pv_yeald = gdf_pv_morocco_utm29n['pv_yeald'].iloc[list_index_intersection_pv].sum()/len(list_index_intersection_pv)

    array_pv_yeald = np.append(array_pv_yeald, pv_yeald)

array_evaluation_pv = (array_pv_yeald / 
                     array_pv_yeald.max()) * 100

#Replace old column with new one
weight_pv = 0.0557
gdf_current_potential['avg_pv_yea'] = array_evaluation_pv * weight_pv
gdf_current_potential['sum'] = gdf_current_potential[['avg_pv_yea','avg_windpo', 
                                                     'water aval', 'industrial',
                                                     'accessibil', 'agricultur',
                                                     'non confli', 'urban_zone',
                                                     'rural_zone']].sum(axis=1) * gdf_current_potential['nogo_zones']

gdf_current_potential.to_file('grid_morocco_h2_pot_test_7.shp', driver='ESRI Shapefile')