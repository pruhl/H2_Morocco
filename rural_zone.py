import geopandas as gpd
import numpy as np

gdf_grid_morocco = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\Python\grid_morocco_clear.shp")

gdf_landuse_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_landuse_a_free_1.shp').to_crs("EPSG:32629")

def list_index(cell,gdf):
    intersects = gdf.intersects(cell)
    return intersects[intersects == True].index.tolist()

array_rural = np.array([])
for i in range(len(gdf_grid_morocco)):
    cell = gdf_grid_morocco.geometry[i]
    list_index_intersection = list_index(cell, gdf_landuse_utm29n)

    area = gdf_landuse_utm29n.loc[list_index_intersection].intersection(cell).area.sum()
    array_rural = np.append(array_rural, area/cell.area if area/cell.area <= 1 else 1)

array_rural -= 1
array_rural = (array_rural/array_rural.min())*100
test
