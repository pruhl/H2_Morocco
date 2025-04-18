import geopandas as gpd

gdf_flh = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Wind_Energiedichte\wind_yeald\Clear_a1_2_3_4.shp")

gdf_flh['FLH_wind'] = gdf_flh[['FLH', 'FLH_2', 'FLH_3', 'FLH_4']].max(axis=1)