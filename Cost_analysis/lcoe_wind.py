import geopandas as gpd
import numpy as np

gdf_wind_morocco_utm29n = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Wind_Energiedichte\wind_yeald\Wind_pot_morocco_FLH.shp").to_crs("EPSG:32629")
gdf_grid_morocco = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\Python\MCA\Grid_morocco\grid_morocco_clear.shp")
gdf_h2_cost_morocco = gpd.read_file('h2_cost_morocco.shp')

capex_wind = 1600 # €/kWp
opex_wind = 0.02 * capex_wind # €/kW

lifetime_wind = 25 # years
r_wind = 0.04 # discount rate

annuity_wind = ((1 + r_wind) ** lifetime_wind * r_wind) / ((1 + r_wind) ** lifetime_wind - 1)

# Calculate the LCOE Wind for each cell

def list_index(gdf, i, grid = gdf_grid_morocco):
    cell = grid['geometry'].iloc[i]
    intersects = gdf.intersects(cell)
    return cell, intersects[intersects == True].index.tolist()

gdf_wind_morocco_utm29n['LCOE_wind [EUR/kWh]'] = (capex_wind * annuity_wind + opex_wind) / gdf_wind_morocco_utm29n['FLH_wind']

array_wind_lcoe = np.array([])
for i in range(len(gdf_grid_morocco)):
    cell_wind, list_index_intersection_wind = list_index(gdf_wind_morocco_utm29n, i)

    if len(list_index_intersection_wind) == 0:
        intersection_next_cell = gdf_wind_morocco_utm29n.dwithin(cell_wind, distance=5001)
        list_intersection_next_cell = intersection_next_cell[intersection_next_cell == True].index.tolist()
        lcoe = gdf_wind_morocco_utm29n['LCOE_wind [EUR/kWh]'].iloc[list_intersection_next_cell].sum()/len(list_intersection_next_cell)
    else:
        lcoe = gdf_wind_morocco_utm29n['LCOE_wind [EUR/kWh]'].iloc[list_index_intersection_wind].sum()/len(list_index_intersection_wind)

    array_wind_lcoe = np.append(array_wind_lcoe, lcoe)

gdf_h2_cost_morocco['LCOE_wind'] = array_wind_lcoe  #nur 10 zeichen erlaubt (eigentlich €/KWh)

gdf_h2_cost_morocco.to_file('h2_cost_morocco.shp', driver='ESRI Shapefile')