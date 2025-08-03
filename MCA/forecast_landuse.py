import geopandas as gpd
import pandas as pd
import numpy as np

# Data
    # Source: FAO, via: https://data.apps.fao.org/catalog/dataset/fad3f475-8973-463f-b56a-e6b6535c1db5  --> Morocco
    # Source: FAO, via: https://data.apps.fao.org/catalog/iso/75aaf5c5-d579-425a-97fb-aa4580536df2      --> Western Sahara
gdf_landuse_mar         = gpd.read_file(r'C:\Users\psclr\Downloads\geonetwork_landcover_mar_gc_adg\mar_gc_adg.shp').to_crs("EPSG:32629") 
gdf_landuse_wsa         = gpd.read_file(r'C:\Users\psclr\Downloads\geonetwork_landcover_wsa_gc_adg\wsa_gc_adg.shp').to_crs("EPSG:32629")
gdf_landuse_concat      = gpd.GeoDataFrame(pd.concat([gdf_landuse_mar, gdf_landuse_wsa]))

gdf_landuse_urban       = gdf_landuse_concat[gdf_landuse_concat['GRIDCODE'].isin([190])]

gdf_morocco_boundary    = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\morocco_Morocco_Country_Boundary.shp").to_crs("EPSG:32629")

# Urbanisation
# Urbanisationrates: 
# Source: "Urban Sustainability Development in Morocco, a Review", via: https://www.mdpi.com/2413-8851/8/2/28
urbanisation = 1.5
goal = gdf_landuse_urban.area.sum() * urbanisation
s = np.sqrt(urbanisation)  # Linear scaling

# Scale of urbanareas
gdf_urban = gdf_landuse_urban.copy()
gdf_urban.geometry = gdf_urban.geometry.scale(
    xfact=s, 
    yfact=s, 
    origin='centroid')

curent_urban_area = gpd.clip(gdf_urban, gdf_morocco_boundary) # Boundary of morocco

delta = 0.01    #1% difference between benchmark and real urbanisation
while (goal - curent_urban_area.area.sum())/goal > delta:
    diff = (goal - curent_urban_area.area.sum())/goal
    s = np.sqrt(1 + diff)
    curent_urban_area.geometry = curent_urban_area.geometry.scale(xfact=s, yfact=s, origin='centroid')
    curent_urban_area = gpd.clip(curent_urban_area, gdf_morocco_boundary)
    if (goal - curent_urban_area.area.sum())/goal < delta:
        break

gdf_landuse_concat[gdf_landuse_concat['GRIDCODE'].isin([190])] = curent_urban_area

gdf_landuse_concat[gdf_landuse_concat['GRIDCODE'] != 190].overlay(gdf_landuse_concat[gdf_landuse_concat['GRIDCODE'].isin([190])], how = 'difference')

gdf_landuse_concat.to_file('Data/morocco_landuse_2050.shp', driver='ESRI Shapefile')