import geopandas as gpd
import numpy as np

gdf_grid_morocco = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\Python\grid_morocco_clear.shp")
gdf_landuse_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_landuse_a_free_1.shp').to_crs("EPSG:32629")


gdf_nogo_zones = gdf_landuse_utm29n[gdf_landuse_utm29n['fclass'].isin(['military', 'nature_reserve', 'recreation_ground'])]

array_nogo = np.array([])
for i in range(len(gdf_grid_morocco)):
    cell = gdf_grid_morocco['geometry'].iloc[i]
    cell_intersection = gdf_nogo_zones.intersects(cell)
    list_index_intersection = cell_intersection[cell_intersection == True].index.tolist()

    array_nogo = np.append(array_nogo, 0 if any(list_index_intersection) else 1)