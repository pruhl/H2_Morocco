import numpy as np
import pandas as pd
import geopandas as gpd

#Weights
dict_weights = {'avg_pv_yeald': 0.017, 
                'avg_windpower': 0.024, 
                're_projects': 0.0547,
                'h2_projects': 0.0894,
                'surface_water': 0.06,
                'groundwater': 0.02,
                'seawater_desalinationplants': 0.27,
                'distance_to_power_grid': 0.0473,
                'pipelines': 0.0334,
                'distance_to_export_ports': 0.0162,
                'accessibility': 0.0162,
                'agricultural_land_share': 0.0153,
                'urban_zone_share': 0.0123,
                'industrial_zone_share': 0.1182,
                'rural_zone_share': 0.0251,
                'population_density': 0.0413,
                'non_conflict_areas': 0.0175,
                'fundings': 0.1224}

#Empty Grid
gdf_grid_morocco = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\gitter_morocco.shp")
gdf_grid_morocco_centroid = gdf_grid_morocco.centroid