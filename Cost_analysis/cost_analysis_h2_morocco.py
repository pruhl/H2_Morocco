import geopandas as gpd 
import numpy as np
import pandas as pd

#Data
    #Grid
gdf_grid_morocco = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\Python\grid_morocco_clear.shp")
gdf_grid_morocco_centroid = gdf_grid_morocco.centroid

def list_index(gdf, i, grid = gdf_grid_morocco):
    cell = grid['geometry'].iloc[i]
    intersects = gdf.intersects(cell)
    return cell, intersects[intersects == True].index.tolist()
#Distance all cells to all cells
list_distance = []
for i in range(len(gdf_grid_morocco)):
    
    d = gdf_grid_morocco_centroid.distance(gdf_grid_morocco_centroid[i])
    list_distance.append(d)

df_distance = pd.DataFrame(list_distance)

# Watercost
lcowater_groundwater = 1 # €/m³
lcowater_desalination = 5 # €/m³
lcowater_surfacewater = 2 # €/m³

#LCOE PV

#LCOE Wind

#Grid Cost

#H2 Pipeline Cost

#H2 Trailer Cost

#Water Pipline Cost

#Water Trailer Cost

#Calcuation of LCOH (cheepest option for each cell)

