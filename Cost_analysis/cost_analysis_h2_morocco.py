import geopandas as gpd 
import numpy as np
import pandas as pd

#Data
    #Curent cost map
gdf_h2_cost                 = gpd.read_file('Maps/h2_cost_morocco.shp')
gdf_h2_cost_centroid        = gdf_h2_cost.geometry.centroid
    #Industrial ports
gdf_ports                   = gpd.read_file("Data/industrial_ports_morocco.shp").to_crs(gdf_h2_cost.crs)
    #RE and Eletrolysis data
gdf_re_data                 = gpd.read_file('Data/data_re_flh_electrolyzer.shp').to_crs(gdf_h2_cost.crs)
df_re_flh                   = pd.read_csv('Data/flh_re.csv')
df_re_flh_cell              = pd.read_csv('Data/cell_flh_re.csv')

#Distance all cells to all cells
list_distance = []
for i in range(len(gdf_h2_cost)):
    list_distance.append(gdf_h2_cost_centroid.distance(gdf_h2_cost_centroid[i]))

df_distance_cells = pd.DataFrame(list_distance)
df_distance_cells = df_distance_cells / 1000  # Convert to km

#Distance all cells to ports
list_distance_ports = []
for i in range(len(gdf_h2_cost)):
    list_distance_ports.append(min(gdf_ports.distance(gdf_h2_cost_centroid[i])))

df_distance_ports = pd.DataFrame(list_distance_ports)
df_distance_ports = df_distance_ports/1000  # Convert to km

#Assumptions
    #Electrolysis
p_nom_el    = 100               # [MW]
eff_el      = 0.7               # [–]
capex_el    = 1000000           # [€/MW]
opex_el     = 0.02 * capex_el   # [€/MW/a]
r_el        = 0.04              # discount rate
lifetime_el = 20                # [a]
annuity_el  = (((1 + r_el) ** lifetime_el * r_el)
                / ((1 + r_el) ** lifetime_el - 1)) * p_nom_el * capex_el    # €/a
annual_cost_el = annuity_el + opex_el * p_nom_el  # €/a

# Watercost
lco_gw      = 1     # €/m³
lco_desal   = 5     # €/m³
lco_sw      = 2     # €/m³

# PV Cost
p_nom_pv  = gdf_re_data['PV']   # [MW]
capex_pv = 1000000              # [€/MWp]
opex_pv = 0.02 * capex_pv       # [€/MWp/a]
lifetime_pv = 25                # [a]
r_pv = 0.04                     # discount rate
annuity_pv = (((1 + r_pv) ** lifetime_pv * r_pv) / 
              ((1 + r_pv) ** lifetime_pv - 1)) * p_nom_pv * capex_pv # €/a
annual_cost_pv = annuity_pv + opex_pv * p_nom_pv  # €/a

# Wind Cost
p_nom_wind = gdf_re_data['Wind']    # [MW]
capex_wind = 1600000                # [€/MW]
opex_wind = 0.02 * capex_wind       # [€/MW]
lifetime_wind = 25                  # [a]
r_wind = 0.04                       # discount rate
annuity_wind = (((1 + r_wind) ** lifetime_wind * r_wind) / 
                ((1 + r_wind) ** lifetime_wind - 1)) * capex_wind * p_nom_wind # €/a
annual_cost_wind = annuity_wind + opex_wind * p_nom_wind  # €/a

gdf_re_data['Cost_pv [EUR/a]'] = annual_cost_pv
gdf_re_data['Cost_wind [EUR/a]'] = annual_cost_wind
gdf_re_data['Cost_re [EUR/a]'] = annual_cost_pv + annual_cost_wind

#Grid Cost
capex_dc_line       = 1500000/4                                 # €/km/MW
capex_converter     = 200000                                    # €/MW
lifetime_dc         = 40                                        # years
opex_dc_line        = 0.01 * capex_dc_line * p_nom_el           # €/km/a
opex_converter      = 0.01 * capex_converter * p_nom_el * 2     # €/a
r_dc                = 0.04                                      # discount rate
annuity_dc_line     = (((1 + r_dc) ** lifetime_dc * r_dc) 
                       / ((1 + r_dc) ** lifetime_dc - 1)) * p_nom_el * capex_dc_line            # €/km/a
annuity_converrter  = (((1 + r_dc) ** lifetime_dc * r_dc) 
                           / ((1 + r_dc) ** lifetime_dc - 1)) * p_nom_el * 2 * capex_converter  # €/a
annual_cost_converter = annuity_converrter + opex_converter # €/a
annual_cost_dc_line = annuity_dc_line + opex_dc_line        # €/km/a

df_dc_cost_cells = df_distance_cells * annual_cost_dc_line + annual_cost_converter

#H2 Pipeline Cost
capex_h2_pipe       = 0.988 * 1000              # €/km/MW_h2
h2_pipe_lifetime    = 40                        # years
opex_h2             = 0.01 * capex_h2_pipe       # €//km/MW_h2/a
r_h2_pipe           = 0.04                      # discount rate
annuity_h2_pipe     = (((1 + r_h2_pipe) ** h2_pipe_lifetime * r_h2_pipe) 
                       / ((1 + r_h2_pipe) ** h2_pipe_lifetime - 1)) * p_nom_el * eff_el * capex_h2_pipe # €/km/a
annual_cost_h2_pipe = annuity_h2_pipe + opex_h2 * p_nom_el * eff_el  # €/km/a

df_h2_pipe_cost_cells = df_distance_ports * annual_cost_h2_pipe

#H2 Trailer Cost --> coming soon!

#Water Pipline Cost --> coming soon!

#Calcuation of LCOH (cheepest option for each cell)
list_h2_electrolysis = []
list_h2_electricity = []
list_h2_pipe = []
list_index_cell = []
list_el_source = []
list_h2_cost = []

#Zuweisung der RE Quelle
df_cost_cells = pd.DataFrame()
for i in range(len(gdf_h2_cost_centroid)):
    # d = gdf_re_data.distance(gdf_h2_cost_centroid[i])
    # idx = d.idxmin()  # Index of the closest RE source
    ref_points = df_re_flh[['FLH_PV', 'FLH_Wind']].values
    comp_point = df_re_flh_cell.iloc[i].values
    d = np.sqrt(np.sum((ref_points - comp_point) ** 2, axis=1))
    idx = np.argmin(d)
    df_cost_cells.at[i, 'Cost_re [EUR/a]'] = gdf_re_data.at[idx, 'Cost_re [EUR/a]']
    df_cost_cells.at[i, 'FLH_electrolyzer'] = gdf_re_data.at[idx, 'FLH_electr']


for i in range(len(gdf_h2_cost)):
    cost_cell = (annual_cost_el + df_dc_cost_cells[i] + df_cost_cells['Cost_re [EUR/a]'] + df_h2_pipe_cost_cells.iat[i, 0])/(df_cost_cells['FLH_electrolyzer']*p_nom_el*eff_el)  # Cost per MWh_h2 for cell 1
    idx_cell = cost_cell.idxmin()  # Index of the cell with the lowest cost for the cell
    cost = cost_cell.min()
    df_cost_cells.at[i, 'index_source_cell'] = idx_cell  # Store the index of the source cell
    df_cost_cells.at[i, 'H2 Price [EUR/MWh_h2]'] = cost  # Store the H2 price for the cell

gdf_cost_cells = gpd.GeoDataFrame(df_cost_cells, geometry=gdf_h2_cost.geometry, crs=gdf_h2_cost.crs)
gdf_cost_cells.to_file('Maps/h2_cost_morocco_4.shp', driver='ESRI Shapefile')

#     list_h2_electricity.append(cost_elektrycity_min)
#     list_index_cell.append(index_cell)
#     list_el_source.append(source_el)
#     list_h2_electrolysis.append(cost_el_h2)
#     list_h2_pipe.append(cost_h2_pipe)
#     list_h2_cost.append(h2_price)

# df_h2_cost = pd.DataFrame(
#     {'Electricity [EUR/MWh_h2]': list_h2_electricity,
#      'Electrolysis [EUR/MWh_h2]': list_h2_electrolysis,
#      'Pipeline [EUR/MWh_h2]': list_h2_pipe,
#      'H2 Price [EUR/MWh_h2]': list_h2_cost, 
#      'index_source_el': list_index_cell, 
#      'source_el': list_el_source})

# #gdf_h2_cost = gdf_h2_cost.join(df_h2_cost)
# gdf_h2_cost['Electricit'] = list_h2_electricity
# gdf_h2_cost['Electrolys'] = list_h2_electrolysis
# gdf_h2_cost['Pipeline ['] = list_h2_pipe
# gdf_h2_cost['H2 Price ['] = list_h2_cost
# gdf_h2_cost['index_sour'] = list_index_cell
# gdf_h2_cost['source_el'] = list_el_source

# gdf_h2_cost['H2 Price ['] = gdf_h2_cost['H2 Price ['].round(2)

# gdf_h2_cost.to_file('h2_cost_morocco_2.shp', driver='ESRI Shapefile')