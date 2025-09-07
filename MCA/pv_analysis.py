import geopandas as gpd
import numpy as np
import pandas as pd

from custom import list_index

# Data
    # Current potential
gdf_current_potential = gpd.read_file('Maps/mca_h2_morocco_2025.shp')
    # PV
    # Source: Global solar atlas
gdf_pv_morocco_utm29n = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Morocco_GISdata_LTAy_YearlyMonthlyTotals_GlobalSolarAtlas-v2_GEOTIFF\PV_yeald_clear_ma_we.shp").to_crs("EPSG:32629")

array_pv_yeald = np.array([])
for i in range(len(gdf_current_potential)):
    cell_pv, list_index_intersection_pv = list_index(gdf_pv_morocco_utm29n, i, gdf_current_potential)

    if len(list_index_intersection_pv) == 0:
        pv_yeald = 0
    else:
        pv_yeald = gdf_pv_morocco_utm29n['pv_yeald'].iloc[list_index_intersection_pv].sum()/len(list_index_intersection_pv)

    array_pv_yeald = np.append(array_pv_yeald, pv_yeald)

df_pv_yeald = pd.DataFrame(data = array_pv_yeald)

df_pv_yeald.to_csv('Data/results_pv_yeald.csv', index=False)