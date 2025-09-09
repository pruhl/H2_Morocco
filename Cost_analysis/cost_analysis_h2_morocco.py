import geopandas as gpd 
import numpy as np
import pandas as pd

#Data
    # Current cost map
gdf_h2_cost                 = gpd.read_file('Maps/h2_cost_morocco.shp')
gdf_h2_cost_centroid        = gdf_h2_cost.geometry.centroid
    # Industrial ports
    # Source: OSM, via QGIS
gdf_ports                   = gpd.read_file("Data/industrial_ports_morocco_2025.shp").to_crs(gdf_h2_cost.crs)
    # RE and Eletrolysis data, FLH electrolyzer, flh pv und wind, Leistung PV und Wind
    # Via Pypsa
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
        # 2025
p_nom_el    = 100               # [MW]
eff_el_2025      = 0.6          # [–] # Source: https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2020/Dec/IRENA_Green_hydrogen_cost_2020.pdf
capex_el_2025    = 1000000      # [€/MW] # Source: https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2020/Dec/IRENA_Green_hydrogen_cost_2020.pdf
opex_el_2025     = 0.05 * capex_el_2025   # [€/MW/a] # Source: https://wupperinst.org/fileadmin/redaktion/downloads/projects/MENA-Fuels_Teilbericht_12_Handelsmodell.pdf
r        = 0.08                 # discount rate # Source: https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2020/Dec/IRENA_Green_hydrogen_cost_2020.pdf
lifetime_el_2025 = 10           # [a] # Source: https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2020/Dec/IRENA_Green_hydrogen_cost_2020.pdf
        # 2050
p_nom_el    = 100               # [MW]
eff_el_2050 = 0.8               # [–] # Source: https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2020/Dec/IRENA_Green_hydrogen_cost_2020.pdf
capex_el_2050    = 200000       # [€/MW] # Source: https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2020/Dec/IRENA_Green_hydrogen_cost_2020.pdf, 2050 dann 200€/kW
opex_el_2050     = 0.05 * capex_el_2025   # [€/MW/a] # Source: https://wupperinst.org/fileadmin/redaktion/downloads/projects/MENA-Fuels_Teilbericht_12_Handelsmodell.pdf
lifetime_el_2050 = 15           # [a] # Source: https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2020/Dec/IRENA_Green_hydrogen_cost_2020.pdf
  
    # Berechnung der jährlichen Kosten
annuity_el_2025  = (((1 + r) ** lifetime_el_2025 * r)
                / ((1 + r) ** lifetime_el_2025 - 1)) * p_nom_el * capex_el_2025    # €/a
annual_cost_el_2025 = annuity_el_2025 + opex_el_2025 * p_nom_el  # €/a

# Watercost
lco_gw      = 0.4     # €/m³ Source: https://www.semanticscholar.org/paper/Simulating-Groundwater-Charges-for-the-Moroccan-Heidecke-Kuhn/795ae1a2b6b6d82f5920522eb9f85b93cebde441
lco_desalination   = 1     # €/m³ Source: Economic concepts to address future water supply–demand imbalances in Iran, Morocco and Saudi Arabia (ist schon im Latex drin)
lco_sw      = 0.19     # €/m³ Source: Economic concepts to address future water supply–demand imbalances in Iran, Morocco and Saudi Arabia (ist schon im Latex drin)

# Watercost pricing for 2050 and if no water is available
lco_gw_2050      = lco_gw *      # €/m³
lco_desalination_2050   = lco_desalination  *   # €/m³
lco_sw_2050      = lco_sw *    # €/m³

# PV Cost
p_nom_pv  = gdf_re_data['PV']   # [MW]
capex_pv_2025 = 691000               # [€/MWp] Source: https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2025/Jul/IRENA_TEC_RPGC_in_2024_2025.pdf
capex_pv_2050 = 423000               # [€/MWp] Source: https://wupperinst.org/fileadmin/redaktion/downloads/projects/MENA-Fuels_Teilbericht_12_Handelsmodell.pdf
opex_pv_2025 = 0.02 * capex_pv_2025       # [€/MWp/a] Annahme
opex_pv_2050 = 0.02 * capex_pv_2050       # [€/MWp/a] Annahme
lifetime_pv = 25                # [a] Annahme
annuity_pv_2025 = (((1 + r) ** lifetime_pv * r) / 
              ((1 + r) ** lifetime_pv - 1)) * p_nom_pv * capex_pv_2025 # €/a
annual_cost_pv_2025 = annuity_pv_2025 + capex_pv_2025 * p_nom_pv  # €/a

# Wind Cost
p_nom_wind = gdf_re_data['Wind']    # [MW]
capex_wind_2025 = 1041000           # [€/MW] Source: https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2025/Jul/IRENA_TEC_RPGC_in_2024_2025.pdf
capex_wind_2050 = 914000           # [€/MW] Source: https://wupperinst.org/fileadmin/redaktion/downloads/projects/MENA-Fuels_Teilbericht_12_Handelsmodell.pdf
opex_wind_2025 = 0.02 * capex_wind_2025       # [€/MW] Annahme
opex_wind_2050 = 0.02 * capex_wind_2050       # [€/MW] Annahme
lifetime_wind = 25                  # [a] Annahme

annuity_wind = (((1 + r) ** lifetime_wind * r) / 
                ((1 + r) ** lifetime_wind - 1)) * capex_wind_2025 * p_nom_wind # €/a
annual_cost_wind = annuity_wind + opex_wind_2025 * p_nom_wind  # €/a

gdf_re_data['Cost_pv [EUR/a]'] = annual_cost_pv
gdf_re_data['Cost_wind [EUR/a]'] = annual_cost_wind
gdf_re_data['Cost_re [EUR/a]'] = annual_cost_pv + annual_cost_wind

#Grid Cost
capex_dc_line_2025       = 1500000                                   # €/km/MW Source: https://www.netzentwicklungsplan.de/sites/default/files/paragraphs-files/Kostenschaetzungen_NEP_2030_2_Entwurf.pdf
capex_converter_2025     = 200000                                    # €/MW Source: https://www.netzentwicklungsplan.de/sites/default/files/paragraphs-files/Kostenschaetzungen_NEP_2030_2_Entwurf.pdf
capex_dc_line_2050       = 2000000                                   # €/km/MW Source: https://www.netzentwicklungsplan.de/sites/default/files/2023-02/NEP_2035_2021_1_Entwurf_Kostenschaetzungen_0.pdf
capex_converter_2050     = 300000                                    # €/MW Source: https://www.netzentwicklungsplan.de/sites/default/files/2023-02/NEP_2035_2021_1_Entwurf_Kostenschaetzungen_0.pdf
lifetime_dc         = 40                                        # years Source: https://plus.netzausbau.de/N2000/DE/Technik/Freileitungen/freileitungen-node.html
opex_dc_line        = 0.01 * capex_dc_line * p_nom_el           # €/km/a
opex_converter      = 0.01 * capex_converter * p_nom_el * 2     # €/a
annuity_dc_line     = (((1 + r) ** lifetime_dc * r) 
                       / ((1 + r) ** lifetime_dc - 1)) * p_nom_el * capex_dc_line            # €/km/a
annuity_converrter  = (((1 + r) ** lifetime_dc * r) 
                           / ((1 + r) ** lifetime_dc - 1)) * p_nom_el * 2 * capex_converter  # €/a
annual_cost_converter = annuity_converrter + opex_converter # €/a
annual_cost_dc_line = annuity_dc_line + opex_dc_line        # €/km/a

df_dc_cost_cells = df_distance_cells.where(df_distance_cells.isnull(), df_distance_cells * annual_cost_dc_line + annual_cost_converter) 

#H2 Pipeline Cost
capex_h2_pipe_2025  = 0.988 * 1000         # €/km/MW_h2 Source: https://www.sciencedirect.com/science/article/pii/S030626192300733X?ref=pdf_download&fr=RR-2&rr=97c7db524cd03633
capex_h2_pipe_2050  = 0.497 * 1000         # €/km/MW_h2 Source: https://www.sciencedirect.com/science/article/pii/S030626192300733X?ref=pdf_download&fr=RR-2&rr=97c7db524cd03633
h2_pipe_lifetime    = 40                        # years
opex_h2             = 0.01 * capex_h2_pipe      # €//km/MW_h2/a
annuity_h2_pipe     = (((1 + r) ** h2_pipe_lifetime * r) 
                       / ((1 + r) ** h2_pipe_lifetime - 1)) * p_nom_el * eff_el * capex_h2_pipe # €/km/a
annual_cost_h2_pipe = annuity_h2_pipe + opex_h2 * p_nom_el * eff_el  # €/km/a

df_h2_pipe_cost_cells = df_distance_ports * annual_cost_h2_pipe

#Zuweisung der RE Quelle
df_cost_cells = pd.DataFrame()
for i in range(len(gdf_h2_cost_centroid)):
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
# gdf_cost_cells.to_file('Maps/h2_cost_morocco_4.shp', driver='ESRI Shapefile')