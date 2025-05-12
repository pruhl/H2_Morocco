import geopandas as gpd 
import numpy as np
import pandas as pd

#Data
    #Grid
gdf_h2_cost                 = gpd.read_file('h2_cost_morocco.shp')
gdf_h2_cost_centroid        = gdf_h2_cost.geometry.centroid
gdf_ports                   = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Esri Shapefile\industrial_port.shp").to_crs(gdf_h2_cost.crs)
gdf_morocco_boundary        = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\morocco_Morocco_Country_Boundary.shp").to_crs(gdf_h2_cost.crs)

#Distance all cells to all cells
list_distance = []
for i in range(len(gdf_h2_cost)):
    d = gdf_h2_cost_centroid.distance(gdf_h2_cost_centroid[i])
    list_distance.append(d)

df_distance_cells = pd.DataFrame(list_distance)

#Distance all cells to ports
# intersections = gdf_ports.intersects(gdf_morocco_boundary)
# gdf_ports = gdf_ports[intersections] 
list_distance_ports = []
for i in range(len(gdf_h2_cost)):
    d = min(gdf_ports.distance(gdf_h2_cost_centroid[i]))
    list_distance_ports.append(d)

df_distance_ports = pd.DataFrame(list_distance_ports)

#Case
p_nom_el    = 100   # MW
eff_el      = 0.7   # efficiency of electrolysis
flh_el_pv   = 3000  # full load hours of electrolysis with PV
flh_el_wind = 4000  # full load hours of electrolysis with windpower
capex_el    = 1000 * 1000  # €/MW
opex_el     = 0.02 * capex_el  # €/MW
el_r        = 0.04  # discount rate
el_lifetime = 20    # years
el_annuity  = (((1 + el_r) ** el_lifetime * el_r)
                / ((1 + el_r) ** el_lifetime - 1)) * p_nom_el # €/a
opex_el = opex_el * p_nom_el # €/a
# Watercost
lco_gw      = 1     # €/m³
lco_desal   = 5     # €/m³
lco_sw      = 2     # €/m³
#LCOE
lcoe_pv         = gdf_h2_cost['LCOE_pv'] * 1000         # €/MWh/a
lcoe_wind       = gdf_h2_cost['LCOE_wind'] * 1000       # €/MWh/a
el_cost_pv      = lcoe_pv * flh_el_pv * p_nom_el        # €/a
el_cost_wind    = lcoe_wind * flh_el_wind * p_nom_el    # €/a
#Grid Cost
dc_line_cost        = 1500000/4                                 # €/km/MW
dc_converter_cost   = 200000                                    # €/MW
dc_lifetime         = 40                                        # years
dc_opex             = 0.01 * dc_line_cost * p_nom_el            # €/km/a
dc_opex_converter   = 0.01 * dc_converter_cost * p_nom_el * 2   # €/a
dc_r                = 0.04                                      # discount rate
dc_annuity          = (((1 + dc_r) ** dc_lifetime * dc_r) 
                       / ((1 + dc_r) ** dc_lifetime - 1)) * p_nom_el * dc_line_cost                 # €/km/a
dc_converter_annuity = (((1 + dc_r) ** dc_lifetime * dc_r) 
                           / ((1 + dc_r) ** dc_lifetime - 1)) * p_nom_el * 2 * dc_converter_cost    # €/a
anual_cost_converter = dc_converter_annuity + dc_opex_converter # €/a
#H2 Pipeline Cost
h2_pipe_cost        = 0.988 * 1000              # €/km/MW_h2
h2_pipe_lifetime    = 40                        # years
h2_pipe_opex        = 0.01 * dc_line_cost       # €/MW
h2_pipe_r           = 0.04                      # discount rate
h2_pipe_annuity     = (((1 + h2_pipe_r) ** h2_pipe_lifetime * h2_pipe_r) 
                       / ((1 + h2_pipe_r) ** h2_pipe_lifetime - 1)) * p_nom_el * eff_el * h2_pipe_cost # €/km/a
#H2 Trailer Cost --> coming soon!

#Water Pipline Cost --> coming soon!

#Calcuation of LCOH (cheepest option for each cell)
list_h2_electrolysis = []
list_h2_electricity = []
list_h2_pipe = []
list_index_cell = []
list_el_source = []
list_h2_cost = []
for i in range(len(gdf_h2_cost)):
    pv_cost         = ((el_cost_pv + df_distance_cells[i] * (dc_annuity + dc_opex) + anual_cost_converter)/
                       (p_nom_el * eff_el * flh_el_pv))
    pv_min          = min(pv_cost)
    index_pv_min    = pv_cost.idxmin()        
    wind_cost       = ((el_cost_wind + df_distance_cells[i] * (dc_annuity + dc_opex) + anual_cost_converter)/
                       (p_nom_el * eff_el * flh_el_wind))
    wind_min        = min(wind_cost)
    index_wind_min  = wind_cost.idxmin()
    
    cost_elektrycity_min    = min(pv_min, wind_min)
    index_cell              = index_pv_min if cost_elektrycity_min == pv_min else index_wind_min
    source_el               = 'PV' if cost_elektrycity_min == pv_min else 'Wind'
    
    cost_el_h2              = el_annuity/(p_nom_el * eff_el * flh_el_pv) if source_el == 'PV' else el_annuity/(p_nom_el * eff_el * flh_el_wind)
    cost_el_h2              += opex_el/(p_nom_el * eff_el * flh_el_pv) if source_el == 'PV' else opex_el/(p_nom_el * eff_el * flh_el_wind)

    cost_h2_pipe            = df_distance_ports.iat[i,0] * h2_pipe_annuity / (p_nom_el * eff_el * flh_el_pv) if source_el == 'PV' else df_distance_ports.iat[i,0] * h2_pipe_annuity / (p_nom_el * eff_el * flh_el_wind)

    h2_price = cost_elektrycity_min + cost_el_h2 + cost_h2_pipe

    list_h2_electricity.append(cost_elektrycity_min)
    list_index_cell.append(index_cell)
    list_el_source.append(source_el)
    list_h2_electrolysis.append(cost_el_h2)
    list_h2_pipe.append(cost_h2_pipe)
    list_h2_cost.append(h2_price)

df_h2_cost = pd.DataFrame(
    {'Electricity [EUR/MWh_h2]': list_h2_electricity,
     'Electrolysis [EUR/MWh_h2]': list_h2_electrolysis,
     'Pipeline [EUR/MWh_h2]': list_h2_pipe,
     'H2 Price [EUR/MWh_h2]': list_h2_cost, 
     'index_source_el': list_index_cell, 
     'source_el': list_el_source})


#gdf_h2_cost = gdf_h2_cost.join(df_h2_cost)
gdf_h2_cost['Electricit'] = list_h2_electricity
gdf_h2_cost['Electrolys'] = list_h2_electrolysis
gdf_h2_cost['Pipeline ['] = list_h2_pipe
gdf_h2_cost['H2 Price ['] = list_h2_cost
gdf_h2_cost['index_sour'] = list_index_cell
gdf_h2_cost['source_el'] = list_el_source

gdf_h2_cost['H2 Price ['] = gdf_h2_cost['H2 Price ['].round(2)

gdf_h2_cost.to_file('h2_cost_morocco.shp', driver='ESRI Shapefile')