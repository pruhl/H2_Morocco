import pandas as pd
import pypsa

#Annahmen
#Eletrolyse (PEM)
p_nom_el = 100000 #kW
eff_el = 0.7 #efficiency
capex_el    = 1000  # €/kW
opex_el     = 0.02 * capex_el  # €/kW
el_r        = 0.04  # discount rate
el_lifetime = 20    # years
el_annuity  = (((1 + el_r) ** el_lifetime * el_r)
                / ((1 + el_r) ** el_lifetime - 1)) * capex_el + opex_el # €/kW

energy_production_min = 3.1e9 # kWh

#PV
df_pv = pd.read_csv('ninja_pv_34.6401_-4.8542_uncorrected.csv', header=3)
df_pv_el = df_pv['electricity']
capex_pv = 1000 # €/kWp
opex_pv = 0.02 * capex_pv # €/kWp
lifetime_pv = 25 # years
r_pv = 0.04 # discount rate

annuity_pv = ((1 + r_pv) ** lifetime_pv * r_pv) / ((1 + r_pv) ** lifetime_pv - 1) * capex_pv + opex_pv # €/kWp

#Wind
df_wind = pd.read_csv('ninja_wind_34.6401_-4.8542_corrected.csv', header=3)
df_wind_el = df_wind['electricity']
capex_wind = 1600 # €/kW
opex_wind = 0.02 * capex_wind # €/kWp
lifetime_wind = 25 # years
r_wind = 0.04 # discount rate
annuity_wind = ((1 + r_wind) ** lifetime_wind * r_wind) / ((1 + r_wind) ** lifetime_wind - 1) * capex_wind + opex_wind # €/kWp

network = pypsa.Network()
network.set_snapshots(range(len(df_pv)))

#Bus

network.add("Bus", name = "bus_electricity")
network.add("Bus", name = "bus_hydrogen")
#Generators
network.add("Generator", name = "pv", bus = "bus_electricity", 
            p_nom_extendable = True, p_max_pu = df_pv_el, capital_cost = annuity_pv)
network.add("Generator", name = "wind", bus = "bus_electricity",
            p_nom_extendable = True, p_max_pu = df_wind_el, capital_cost = annuity_wind)
#Link Electrolyzer
network.add("Link", name = "Electrolyzer", bus0 = "bus_electricity", bus1 = "bus_hydrogen",
            p_nom_extendable = True, efficiency = eff_el, capital_cost = el_annuity)
#Storage
#network.add("StorageUnit", name = "storage_hydrogen", bus = "bus_hydrogen", p_nom_extendable = True)

network.add("Generator", name = "negative_gen", bus = "bus_hydrogen",
             p_nom_extendable = True, sign = -1, e_sum_min = energy_production_min, e_sum_max = energy_production_min)

network.optimize(solver = "gurobi")

