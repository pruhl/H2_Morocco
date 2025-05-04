import geopandas as gpd
import numpy as np

gdf_pv_morocco_utm29n = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Morocco_GISdata_LTAy_YearlyMonthlyTotals_GlobalSolarAtlas-v2_GEOTIFF\PV_yeald_clear_ma_we.shp").to_crs("EPSG:32629")
gdf_grid_morocco = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\Python\MCA\Grid_morocco\grid_morocco_clear.shp")
gdf_h2_cost_morocco = gpd.read_file('h2_cost_morocco.shp')

capex_pv = 1000 # €/kWp
opex_pv = 0.02 * capex_pv # €/kWp

lifetime_pv = 25 # years
r_pv = 0.04 # discount rate

annuity_pv = ((1 + r_pv) ** lifetime_pv * r_pv) / ((1 + r_pv) ** lifetime_pv - 1)

def list_index(gdf, i, grid = gdf_grid_morocco):
    cell = grid['geometry'].iloc[i]
    intersects = gdf.intersects(cell)
    return cell, intersects[intersects == True].index.tolist()
# Calculate the LCOE PV for each cell

gdf_pv_morocco_utm29n['LCOE_pv [EUR/kWh]'] = (capex_pv * annuity_pv + opex_pv) / gdf_pv_morocco_utm29n['pv_yeald']

array_pv_lcoe = np.array([])
for i in range(len(gdf_grid_morocco)):
    cell_pv, list_index_intersection_pv = list_index(gdf_pv_morocco_utm29n, i)

    if len(list_index_intersection_pv) == 0:
        intersection_next_cell = gdf_pv_morocco_utm29n.dwithin(cell_pv, distance=5001)
        list_intersection_next_cell = intersection_next_cell[intersection_next_cell == True].index.tolist()
        lcoe = gdf_pv_morocco_utm29n['LCOE_pv [EUR/kWh]'].iloc[list_intersection_next_cell].sum()/len(list_intersection_next_cell)
    else:
        lcoe = gdf_pv_morocco_utm29n['LCOE_pv [EUR/kWh]'].iloc[list_index_intersection_pv].sum()/len(list_index_intersection_pv)

    array_pv_lcoe = np.append(array_pv_lcoe, lcoe)

gdf_h2_cost_morocco['LCOE_pv'] = array_pv_lcoe #In GDF sind nur 10 zeichen erlaubt

gdf_h2_cost_morocco.to_file('h2_cost_morocco.shp', driver='ESRI Shapefile')