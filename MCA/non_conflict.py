import geopandas as gpd
import numpy as np

gdf_grid_morocco = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\Python\grid_morocco_clear.shp")
gdf_morocco = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\morocco.geojson').to_crs("EPSG:32629").union_all()

intersection = gdf_grid_morocco.intersects(gdf_morocco)

intersection.loc[intersection == True] = 100
intersection.loc[intersection == False] = 0

intersection.astype(float)