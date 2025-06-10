import geopandas as gpd 
import numpy as np
import pandas as pd

#Data
    #Grid
gdf_h2_cost                 = gpd.read_file('h2_cost_morocco.shp')
gdf_h2_cost_centroid        = gdf_h2_cost.geometry.centroid
gdf_ports                   = gpd.read_file("Data/industrial_ports_morocco.shp").to_crs(gdf_h2_cost.crs)

#Distance all cells to all cells
list_distance = []
for i in range(len(gdf_h2_cost)):
    d = gdf_h2_cost_centroid.distance(gdf_h2_cost_centroid[i])
    list_distance.append(d)

df_distance_cells = pd.DataFrame(list_distance)

#FLH each cell from pv_wind each cell --> Nochmals zu verbessern!oder kontrollieren
for j in range(len(gdf_h2_cost)):
    list_flh_el = []
    for i in range(len(gdf_h2_cost)):
        pv_flh = gdf_h2_cost.at[i, 'FLH_pv']
        wind_flh = gdf_h2_cost.at[j, 'FLH_wind']
        flh_electrolysis = (
            -6.6770138990268e-05 * pv_flh
            + 0.0009983995228525259 * wind_flh
            - 0.0792907929992582 * pv_flh**2
            + 0.6015039377643137 * pv_flh * wind_flh
            - 0.17342074638805446 * wind_flh**2
            + 0.00023937794024431227 * pv_flh**3
            - 0.0006510799366329 * pv_flh**2 * wind_flh
            + 0.00019244450456020793 * pv_flh * wind_flh**2
            - 1.816467055199652e-06 * wind_flh**3
            - 8.5611244271594e-08 * pv_flh**4
            + 1.7739890917961985e-07 * pv_flh**3 * wind_flh
            - 5.4292976076750066e-08 * pv_flh**2 * wind_flh**2
            + 1.3219706105279685e-09 * pv_flh * wind_flh**3
            - 4.5916292049454945e-11 * wind_flh**4
            - 244026.2227515451
        )
        list_flh_el.append(flh_electrolysis)
        if i == len(gdf_h2_cost) - 1:
            gdf_h2_cost.at[j, 'FLH_el'] = max(list_flh_el)

#Distance all cells to ports
list_distance_ports = []
for i in range(len(gdf_h2_cost)):
    d = min(gdf_ports.distance(gdf_h2_cost_centroid[i]))
    list_distance_ports.append(d)

df_distance_ports = pd.DataFrame(list_distance_ports)

#Case
p_nom_el    = 100               # MW
eff_el      = 0.7               # efficiency of electrolysis
flh_el_pv   = 3000              # full load hours of electrolysis with PV
flh_el_wind = 4000              # full load hours of electrolysis with windpower
capex_el    = 1000 * 1000       # €/MW
opex_el     = 0.02 * capex_el   # €/MW
el_r        = 0.04              # discount rate
el_lifetime = 20                # years
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

gdf_h2_cost.to_file('h2_cost_morocco_2.shp', driver='ESRI Shapefile')