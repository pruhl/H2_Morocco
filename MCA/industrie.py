import geopandas as gpd

# Data
    # Current potential
gdf_grid = gpd.read_file('Grid_morocco/grid_morocco_clear.shp')
    # Industrial
    # Source: OSM, via QGIS
gdf_landuse_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_landuse_a_free_1.shp').to_crs("EPSG:32629")

gdf_industrie_morocco = gdf_landuse_utm29n[gdf_landuse_utm29n['fclass'].isin(['industrial'])].union_all()

ds_intersection_industrie = (gdf_grid.intersection(gdf_industrie_morocco).area/
                              gdf_grid.area)

ds_intersection_industrie.to_csv('results/results_industrie.csv', index=False)