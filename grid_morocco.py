import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon

gdf_morocco_boundary = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\morocco_Morocco_Country_Boundary.shp")
gdf_morocco_boundary_utm29N = gdf_morocco_boundary.to_crs("EPSG:32629")

gdf_morocco_boundary.plot()
gdf_morocco_boundary_utm29N.plot()


def grid_cration(polygon, cell_size):
    min_x, min_y, max_x, max_y = polygon.total_bounds
    
    # Gitterpunkte
    x_coords = np.arange(min_x, max_x, cell_size)
    y_coords = np.arange(min_y, max_y, cell_size)
    
    # Erzeuge eine Liste von Polygonen für jede Zelle im rechteckigen Gitter
    grid_polygons = []
    for x in x_coords:
        for y in y_coords:
            cell = Polygon([
                (x, y),
                (x + cell_size, y),
                (x + cell_size, y + cell_size),
                (x, y + cell_size)
            ])

            if polygon.geometry.intersects(cell).any():
                grid_polygons.append(cell)

    return gpd.GeoDataFrame(geometry=grid_polygons, crs="EPSG:32629")

grid_size = 10000
gdf_morocco_gird = grid_cration(polygon=gdf_morocco_boundary_utm29N, cell_size=grid_size)

gdf_morocco_gird.plot()

gdf_morocco_gird.to_file("gitter_morocco.shp", driver='ESRI Shapefile')