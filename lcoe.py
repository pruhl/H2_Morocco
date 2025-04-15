import geopandas as gpd
import pandas as pd
import numpy as np

gdf_pv_morocco_utm29n = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Morocco_GISdata_LTAy_YearlyMonthlyTotals_GlobalSolarAtlas-v2_GEOTIFF\PV_yeald_clear.shp").to_crs("EPSG:32629")

capex_pv = 1200 # €/kWp
opex_pv = 0.02 * capex_pv # €/kWp

lifetime_pv = 25 # years
r_pv = 0.04 # discount rate

annuity_pv = ((1 + r_pv) ** lifetime_pv * r_pv) / ((1 + r_pv) ** lifetime_pv - 1)

# Calculate the LCOE PV for each cell

gdf_pv_morocco_utm29n['LCOE_pv [€]'] = (capex_pv * annuity_pv + opex_pv) / gdf_pv_morocco_utm29n['pv_yeald']



