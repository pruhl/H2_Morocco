import geopandas as gpd

# Data
    # Current potential
gdf_current_potential = gpd.read_file('Maps/mca_h2_morocco_2025.shp')
    # Industrial
    # Source: OSM, via QGIS
gdf_landuse_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_landuse_a_free_1.shp').to_crs("EPSG:32629")

gdf_industrie_morocco = gdf_landuse_utm29n[gdf_landuse_utm29n['fclass'].isin(['industrial'])].union_all()

ds_intersection_industrie = (gdf_current_potential.intersection(gdf_industrie_morocco).area/
                              gdf_current_potential.area)

ds_intersection_industrie.to_csv('Data/results_industrie.csv', index=False)