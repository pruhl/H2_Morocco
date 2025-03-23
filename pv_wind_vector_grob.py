import geopandas as gpd

gdf_pv_morocco = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Vektor_PV.shp")

gdf_pv_morocco_utm29n = gdf_pv_morocco.to_crs("EPSG:32629")