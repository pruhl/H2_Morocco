import geopandas as gpd

gdf_current_potential = gpd.read_file('Grid_morocco/grid_morocco_clear.shp')

gdf_water_consumption = gpd.read_file('Water_Consumption.shp')
gdf_water_exploitable = gpd.read_file('water_exploitable.shp')

array_water = gdf_water_exploitable['Basin'] * 10**6 - gdf_water_consumption['Water_Cons']
# #Replace old column with new one
# weight_water = 0.3399
# gdf_current_potential['water aval'] = array_water * weight_water
# gdf_current_potential['sum'] = gdf_current_potential[['avg_pv_yea','avg_windpo', 
#                                                      'water aval', 'industrial',
#                                                      'accessibil', 'agricultur',
#                                                      'non confli', 'urban_zone',
#                                                      'rural_zone']].sum(axis=1) * gdf_current_potential['nogo_zones']

# gdf_current_potential.to_file('grid_morocco_h2_pot_test_7.shp', driver='ESRI Shapefile')