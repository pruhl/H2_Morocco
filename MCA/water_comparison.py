import geopandas as gpd
import matplotlib.pyplot as plt

gdf_water_res       = gpd.read_file('Maps/mca_h2_morocco_2025_water_res.shp')
gdf_water_available = gpd.read_file('Maps/mca_h2_morocco_2025_water_available.shp')
gdf_water_50_50     = gpd.read_file('Maps/mca_h2_morocco_2025_water_50_50.shp')

fig, axs = plt.subplots(1, 3, figsize = (15,5))
gdf_water_res.plot(column='sum', cmap = 'RdYlGn', legend = False, vmin=10, vmax=50, ax = axs[0])
axs[0].set_title('Water_res')

gdf_water_50_50.plot(column='sum', cmap = 'RdYlGn', legend = False, vmin=10, vmax=50, ax = axs[1])
axs[1].set_title('Water_50/50')

gdf_water_available.plot(column='sum', cmap = 'RdYlGn', legend = False, vmin=10, vmax=50, ax = axs[2])
axs[2].set_title('Water_available')
