import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx
import pandas as pd

# Data
gdf_morocco_boundary    = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\morocco_Morocco_Country_Boundary.shp").to_crs("EPSG:32629")
df_pv = pd.read_csv('Data/results_pv_yeald.csv')
gdf_grid = gpd.read_file('Grid_morocco/grid_morocco_clear.shp')
gdf_grid['PV'] = df_pv['0']

df_wind = pd.read_csv('Data/results_wind_flh.csv')
gdf_grid['Wind'] = df_wind['0']

# Map PV
fig, ax = plt.subplots(figsize=(15, 10))
gdf_grid.plot(ax = ax, column='PV', cmap='turbo', legend=True, vmin=1000, legend_kwds={"label": "kWh/kWp", "orientation": "vertical"})
cx.add_basemap(ax, crs=gdf_morocco_boundary.crs, source=cx.providers.CartoDB.Positron)
plt.axis('off')
cbar_ax = fig.axes[-1]
cbar_ax.tick_params(labelsize=12)
cbar_ax.yaxis.label.set_size(14)
plt.tight_layout()
plt.savefig("Maps/morocco_photovoltaic_potential.pdf", format="pdf", dpi=300, bbox_inches='tight', pad_inches=0)
plt.show()

# Map Wind
fig, ax = plt.subplots(figsize=(15, 10))
gdf_grid.plot(ax = ax, column='Wind', cmap='turbo', legend=True, legend_kwds={"label": "Hours [h]", "orientation": "vertical"})
cx.add_basemap(ax, crs=gdf_morocco_boundary.crs, source=cx.providers.CartoDB.Positron)
plt.axis('off')
cbar_ax = fig.axes[-1]
cbar_ax.tick_params(labelsize=12)
cbar_ax.yaxis.label.set_size(14)
plt.tight_layout()
plt.savefig("Maps/morocco_wind_potential.pdf", format="pdf", dpi=300, bbox_inches='tight', pad_inches=0)
plt.show()