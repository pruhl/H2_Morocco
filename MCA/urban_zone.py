import geopandas as gpd
import numpy as np

gdf_grid_morocco = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\Python\grid_morocco_clear.shp")
gdf_landuse_utm29n = gpd.read_file(r'C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\Landuse\gis_osm_landuse_a_free_1.shp').to_crs("EPSG:32629")

gdf_urban_morocco = gdf_landuse_utm29n[gdf_landuse_utm29n['fclass'].isin(['residential'])]

array_urban = np.array([])
for i in range(len(gdf_grid_morocco)):
    cell = gdf_grid_morocco['geometry'].iloc[i]
    cell_intersection = gdf_urban_morocco.intersects(cell)
    list_index_intersection = cell_intersection[cell_intersection == True].index.tolist()
    area = gdf_urban_morocco.loc[list_index_intersection].intersection(cell).area.sum()

    array_urban = np.append(array_urban, area/cell.area)

array_urban -= array_urban.max()
array_urban = (array_urban/array_urban.min())*100