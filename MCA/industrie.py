import geopandas as gpd

# Daten einlesen
    #Curent potential map
gdf_current_potential = gpd.read_file('Maps/test_2.shp')
    #Industrial
gdf_landuse_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_landuse_a_free_1.shp').to_crs("EPSG:32629")

gdf_industrie_morocco = gdf_landuse_utm29n[gdf_landuse_utm29n['fclass'].isin(['industrial'])].union_all()

ds_intersection_industrie = (gdf_current_potential.intersection(gdf_industrie_morocco).area/
                              gdf_current_potential.area)

ds_intersection_industrie = (ds_intersection_industrie/ds_intersection_industrie.max())*100

#Replace old column with new one
# weight_indust = 0.16
# gdf_current_potential['industrial'] = gdf_intersection_industrie * weight_indust
# gdf_current_potential['sum'] = gdf_current_potential[['avg_pv_yea','avg_windpo', 
#                                                      'water aval', 'industrial',
#                                                      'accessibil', 'agricultur',
#                                                      'non confli', 'urban_zone',
#                                                      'rural_zone']].sum(axis=1) * gdf_current_potential['nogo_zones']

# gdf_current_potential.to_file('Maps/test_2.shp', driver='ESRI Shapefile')