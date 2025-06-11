import geopandas as gpd 
import numpy as np
import pandas as pd

#Data
    #Grid
gdf_h2_cost                 = gpd.read_file('h2_cost_morocco.shp')
gdf_h2_cost_centroid        = gdf_h2_cost.geometry.centroid
gdf_ports                   = gpd.read_file("Data/industrial_ports_morocco.shp").to_crs(gdf_h2_cost.crs)

#Case
p_nom_el    = 100               # MW
eff_el      = 0.7               # efficiency of electrolysis
capex_el    = 1000 * 1000       # €/MW
opex_el     = 0.02 * capex_el   # €/MW
el_r        = 0.04              # discount rate
el_lifetime = 20                # years
el_annuity  = (((1 + el_r) ** el_lifetime * el_r)
                / ((1 + el_r) ** el_lifetime - 1)) * p_nom_el * capex_el # €/a
opex_el = opex_el * p_nom_el # €/a
cost_electrolyzer = el_annuity + opex_el # €/a

#Grid Cost
dc_line_cost        = 1500000/4                                 # €/km/MW
dc_converter_cost   = 200000                                    # €/MW
dc_lifetime         = 40                                        # years
dc_opex             = 0.01 * dc_line_cost * p_nom_el            # €/km/a
dc_opex_converter   = 0.01 * dc_converter_cost * p_nom_el * 2   # €/a
dc_r                = 0.04                                      # discount rate
capex_dc_annuity          = (((1 + dc_r) ** dc_lifetime * dc_r) 
                       / ((1 + dc_r) ** dc_lifetime - 1)) * p_nom_el * dc_line_cost                 # €/km/a
capex_dc_converter_annuity = (((1 + dc_r) ** dc_lifetime * dc_r) 
                           / ((1 + dc_r) ** dc_lifetime - 1)) * p_nom_el * 2 * dc_converter_cost    # €/a

anual_cost_dc_per_km = capex_dc_annuity + dc_opex # €/km/a
anual_cost_converter = capex_dc_converter_annuity + dc_opex_converter # €/a

#H2 Pipeline Cost
h2_pipe_cost        = 0.988 * 1000              # €/km/MW_h2
h2_pipe_lifetime    = 40                        # years
h2_pipe_opex_per_km        = 0.01 * h2_pipe_cost * p_nom_el * eff_el     # €/km
h2_pipe_r           = 0.04                      # discount rate
h2_pipe_annuity_per_km     = (((1 + h2_pipe_r) ** h2_pipe_lifetime * h2_pipe_r) 
                       / ((1 + h2_pipe_r) ** h2_pipe_lifetime - 1)) * p_nom_el * eff_el * h2_pipe_cost # €/km/a


# PV Cost/Wind 
lcoe_pv         = gdf_h2_cost['LCOE_pv'] * 1000         # €/MWh/a
lcoe_wind       = gdf_h2_cost['LCOE_wind'] * 1000       # €/MWh/a
#H2 Trailer Cost --> coming soon!
annual_h2_trailer_per_km = np.inf

annual_h2_pipe_per_km = h2_pipe_annuity_per_km + h2_pipe_opex_per_km # €/km/a
#Distance all cells to all cells
list_distance = []
for i in range(len(gdf_h2_cost)):
    d = gdf_h2_cost_centroid.distance(gdf_h2_cost_centroid[i])
    list_distance.append(d)

df_distance_cells = pd.DataFrame(list_distance)

#Distance all cells to ports
list_distance_ports = []
for i in range(len(gdf_h2_cost)):
    d = min(gdf_ports.distance(gdf_h2_cost_centroid[i]))
    list_distance_ports.append(d)

df_distance_ports = pd.DataFrame(list_distance_ports)


##################################################
#For-Schleife# for i in range(len(gdf_h2_cost)):
##################################################
cell = df_distance_cells[0]

#Grid
cost_grid_line = df_distance_cells.at[0,i] * anual_cost_dc_per_km + lcoe_pv[i] + lcoe_wind[i]

cost_grid = anual_cost_converter + cost_grid_line # €/a

#Transport
cost_pipeline = annual_h2_pipe_per_km * min(df_distance_ports.at[0])
cost_trailer = annual_h2_trailer_per_km * min(df_distance_ports.at[0]) # Trailer kosten müssen wir noch hinzufügen
cost_transport = min(cost_pipeline, cost_trailer)

#Electricity Cost 

cost_pv = 
cost_elec = cost_grid + cost_pv + cost_wind



h2_cost = (cost_elec + cost_electrolyzer + cost_transport + cost_water)/h2_production