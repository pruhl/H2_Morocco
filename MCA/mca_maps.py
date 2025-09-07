import geopandas as gpd
import matplotlib.pyplot as plt

theme_rating = 'turbo_r'
theme_diff   = 'viridis'

# 50/50 Water/Res
    #2025
gdf_water_50_50         = gpd.read_file('Maps/mca_h2_morocco_2025_water_50_50.shp')
    #2050
gdf_water_50_50_2050    = gpd.read_file('Maps/mca_h2_morocco_2050_water_50_50.shp')
    #Diffs
gdf_water_50_50_diff = gpd.GeoDataFrame(geometry=gdf_water_50_50_2050.geometry, crs = gdf_water_50_50_2050.crs,
                                               data = gdf_water_50_50_2050['sum'] - gdf_water_50_50['sum'])

# Plots with 50/50 rating of water residual and water availability
fig, axs = plt.subplots(3, 1, figsize = (15,15))
fig.suptitle('Wateranalysis (50/50 rating)')
gdf_water_50_50.plot(column='sum', cmap = theme_rating, legend = True, vmin=0, vmax=gdf_water_50_50['sum'].max(), ax = axs[0])
axs[0].set_title('2025')

gdf_water_50_50_2050.plot(column='sum', cmap = theme_rating, legend = True, vmin=0, vmax=gdf_water_50_50['sum'].max(), ax = axs[1])
axs[1].set_title('2050')

gdf_water_50_50_diff.plot(column='sum', cmap = theme_diff, legend = True, ax = axs[2])
axs[2].set_title('Diff')