import geopandas as gpd

# Daten einlesen
    #Curent potential map
gdf_current_potential = gpd.read_file('grid_morocco_h2_pot_test_8.shp')
    #non_conflict
gdf_morocco = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\morocco.geojson').to_crs("EPSG:32629").union_all()

non_conflict = gdf_current_potential.intersects(gdf_morocco)

non_conflict.loc[non_conflict == True] = 100
non_conflict.loc[non_conflict == False] = 0

non_conflict = non_conflict.astype(float)

#Replace old column with new one
weight_non_conflict = 0.1663
gdf_current_potential['non confli'] = non_conflict * weight_non_conflict
gdf_current_potential['sum'] = gdf_current_potential[['avg_pv_yea','avg_windpo', 
                                                     'water aval', 'industrial',
                                                     'accessibil', 'agricultur',
                                                     'non confli', 'urban_zone',
                                                     'rural_zone']].sum(axis=1) * gdf_current_potential['nogo_zones']

gdf_current_potential.to_file('grid_morocco_h2_pot_test_8.shp', driver='ESRI Shapefile')