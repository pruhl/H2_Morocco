import pandas as pd
import geopandas as gpd

gdf_data = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\Python\Cost_analysis\h2_cost_morocco_2.shp')

df_flh_pv_wind = gdf_data[['FLH_pv', 'FLH_wind']]
df_flh_pv_wind.loc[df_flh_pv_wind['FLH_wind'] > 5000, 'FLH_wind'] = 5000  # Limit wind FLH to 5000
df_flh_pv_wind.loc[df_flh_pv_wind['FLH_pv'] > 1950, 'FLH_pv'] = 1950  # Limit PV FLH to 1950
#df_flh_pv_wind['FLH_pv'][df_flh_pv_wind['FLH_pv'] < 1800] = 1800  # Limit PV FLH to 1950
df_flh_pv_wind['FLH_el'] = (0.0*1 +
                            -6.6770138990268e-05*df_flh_pv_wind['FLH_pv'] + 
                            0.0009983995228525259*df_flh_pv_wind['FLH_wind'] + 
                            -0.0792907929992582*df_flh_pv_wind['FLH_pv']**2 + 
                            0.6015039377643137*df_flh_pv_wind['FLH_pv']*df_flh_pv_wind['FLH_wind'] + 
                            -0.17342074638805446*df_flh_pv_wind['FLH_wind']**2 + 
                            0.00023937794024431227*df_flh_pv_wind['FLH_pv']**3 + 
                            -0.0006510799366329*df_flh_pv_wind['FLH_pv']**2*df_flh_pv_wind['FLH_wind'] + 
                            0.00019244450456020793*df_flh_pv_wind['FLH_pv']*df_flh_pv_wind['FLH_wind']**2 + 
                            -1.816467055199652e-06*df_flh_pv_wind['FLH_wind']**3 + 
                            -8.5611244271594e-08*df_flh_pv_wind['FLH_pv']**4 + 
                            1.7739890917961985e-07*df_flh_pv_wind['FLH_pv']**3*df_flh_pv_wind['FLH_wind'] + 
                            -5.4292976076750066e-08*df_flh_pv_wind['FLH_pv']**2*df_flh_pv_wind['FLH_wind']**2 + 
                            1.3219706105279685e-09*df_flh_pv_wind['FLH_pv']*df_flh_pv_wind['FLH_wind']**3 + 
                            -4.5916292049454945e-11*df_flh_pv_wind['FLH_wind']**4 + 
                            -244026.2227515451)

df_flh_pv_wind.loc[df_flh_pv_wind['FLH_el'] < 4000, 'FLH_el'] = 0  # If FLH_el is less than 4000, set it to 0

df_flh_pv_wind['MW_Wind'] = 0.0*1 +2.3488108197027923e-08*df_flh_pv_wind['FLH_wind'] + 7.113553154609071e-05*df_flh_pv_wind['FLH_wind']**2 + -1.4679236320927621e-08*df_flh_pv_wind['FLH_wind']**3 + 8.297602504707571e-13*df_flh_pv_wind['FLH_wind']**4 + -288.41758494153777
df_flh_pv_wind['MW_Pv'] = 0.0*1 +2.547699558547833e-08*df_flh_pv_wind['FLH_pv'] + 7.715902799128186e-05*df_flh_pv_wind['FLH_pv']**2 + -2.347656387286697e-08*df_flh_pv_wind['FLH_pv']**3 + 1.7837178121312628e-12*df_flh_pv_wind['FLH_pv']**4 -1.247296667877137

df_flh_pv_wind.loc[df_flh_pv_wind['MW_Wind'] < 150, 'MW_Wind'] = 0  # If no el, than 0 MW PV and Wind
df_flh_pv_wind.loc[df_flh_pv_wind['MW_Pv']< 50, 'MW_Pv'] = 0  # If no el, than 0 MW PV and Wind
