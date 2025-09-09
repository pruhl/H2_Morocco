import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as cx
import numpy as np
import matplotlib.colors as mcolors

# Min-Max_scale-funtion
def min_max_scale(df):
    return (df - df.min())/(df.max()-df.min())

# Grid morocco
gdf_morocco_boundary    = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\morocco_Morocco_Country_Boundary.shp").to_crs("EPSG:32629")
gdf_mca_morocco_2025 = gpd.read_file('Grid_morocco/grid_morocco_clear.shp').to_crs("EPSG:32629")
gdf_mca_morocco_2050 = gdf_mca_morocco_2025.copy()

# weights
dict_weights_category = {'avg_pv_yeald': 0.0557, 
                         'avg_windpower': 0.1113, 
                         'accessibility': 0.0831,
                         'agricultural_land_share': 0.0194,
                         'urban_zone_share': 0.0148,
                         'industrial_zone_share': 0.16,
                         'rural_zone_share': 0.0496,
                         'water_avalibility': 0.3399,
                         'non_conflict_areas': 0.1663}

dict_weights_roads = {'motorway': 0.25,
                  'trunk': 0.18,
                  'primary':0.12, 
                  'secondary':0.09, 
                  'tertiary':0.06, 
                  'track':0.01, 
                  'track_grade1':0.03, 
                  'track_grade2':0.02, 
                  'track_grade3':0.01, 
                  'track_grade4':0.01, 
                  'unclassified':0.04, 
                  'railway':0.18}

# Read results
df_pv_yeald = pd.read_csv('Data/results_pv_yeald.csv')
df_wind_flh = pd.read_csv('Data/results_wind_flh.csv')
df_accessibility = pd.read_csv('Data/results_accessibility.csv')
df_agriculture = pd.read_csv('Data/results_agriculture.csv')
df_urban = pd.read_csv('Data/results_urban.csv')
df_industrie = pd.read_csv('Data/results_industrie.csv')
df_rural = pd.read_csv('Data/results_rural.csv')
df_water = pd.read_csv('Data/results_water_res_availabil.csv')
df_non_conflict_areas = pd.read_csv('Data/non_conflict_areas.csv')

df_nogo_zones = pd.read_csv('Data/results_nogo_zones.csv')

# Scale results. 
# Water and non colflict already scored

    # PV Yeald
df_pv_yeald = min_max_scale(df_pv_yeald)*100

    # Wind flh
df_wind_flh = min_max_scale(df_wind_flh)*100

    # Accessibility
df_accessibility -= df_accessibility.min()
df_accessibility = df_accessibility/(df_accessibility.max()-df_accessibility.min())
df_accessibility= df_accessibility*100*dict_weights_roads.values()

ds_accessibility_sum = df_accessibility.sum(axis=1).astype(float)

    # Agriculture
df_agriculture = min_max_scale(df_agriculture)*100

    # Urban areas
df_urban = min_max_scale(df_urban)*100

    # Industrie
df_industrie = min_max_scale(df_industrie)*100

    # Rural areas
df_rural = min_max_scale(df_rural)*100

# Results 2025
dict_results = {'avg_pv_yeald': df_pv_yeald.values.flatten(), 
                         'avg_windpower': df_wind_flh.values.flatten(), 
                         'accessibility': ds_accessibility_sum.values.flatten(),
                         'agricultural_land_share': df_agriculture.values.flatten(),
                         'urban_zone_share': df_urban.values.flatten(),
                         'industrial_zone_share': df_industrie.values.flatten(),
                         'rural_zone_share': df_rural.values.flatten(),
                         'water_avalibility': df_water.values.flatten(),
                         'non_conflict_areas': df_non_conflict_areas.values.flatten()}
df_results = pd.DataFrame(dict_results)

df_weighted_results = df_results*dict_weights_category
df_mca_morocco = df_weighted_results.sum(axis = 1) * df_nogo_zones['NoGos']
df_mca_morocco.name = 'MCA_Morocco'

gdf_mca_morocco_2025['Hydrogen_potential'] = df_mca_morocco

# Results 2050
dict_results_2050 = {'avg_pv_yeald': df_pv_yeald.values.flatten(), 
                         'avg_windpower': df_wind_flh.values.flatten(), 
                         'accessibility': ds_accessibility_sum.values.flatten(),
                         'agricultural_land_share': df_agriculture_2050.values.flatten(),
                         'urban_zone_share': df_urban_2050.values.flatten(),
                         'industrial_zone_share': df_industrie.values.flatten(),
                         'rural_zone_share': df_rural_2050.values.flatten(),
                         'water_avalibility': df_water_2050.values.flatten(),
                         'non_conflict_areas': df_non_conflict_areas.values.flatten()}
df_results_2050 = pd.DataFrame(dict_results_2050)

df_weighted_results_2050 = df_results_2050*dict_weights_category
df_mca_morocco_2050 = df_weighted_results_2050.sum(axis = 1) * df_nogo_zones['NoGos']
df_mca_morocco_2050.name = 'MCA_Morocco'

gdf_mca_morocco_2050['Hydrogen_potential'] = df_mca_morocco_2050

### MAPS ###

theme_rating = 'jet_r'
theme_diff   = 'OrRd_r'

# Map MCA 2025
fig, ax = plt.subplots(figsize=(15, 10))
gdf_morocco_boundary.plot(ax=ax, edgecolor='black', facecolor="none", linewidth=1)
gdf_mca_morocco_2025.plot(ax=ax, cmap = theme_rating, column= 'Hydrogen_potential', legend=True, legend_kwds={"label": "Relativ hydrogen potential", "orientation": "vertical"})
cx.add_basemap(ax, crs=gdf_mca_morocco_2025.crs, source=cx.providers.CartoDB.Positron)
plt.title('Hydrogen potential map of Morocco', fontsize = 15)
plt.axis('off')
cbar_ax = fig.axes[-1]
cbar_ax.tick_params(labelsize=12)
cbar_ax.yaxis.label.set_size(12)
# plt.savefig("Maps/mca_morocco.pdf", format="pdf", dpi=300)
plt.show()

# Map MCA 2050
fig, ax = plt.subplots(figsize=(15, 10))
gdf_morocco_boundary.plot(ax=ax, edgecolor='black', facecolor="none", linewidth=1)
gdf_mca_morocco_2050.plot(ax=ax, cmap = theme_rating, column= 'sum', legend=True, legend_kwds={"label": "Relativ hydrogen potential", "orientation": "vertical"})
cx.add_basemap(ax, crs=gdf_mca_morocco_2050.crs, source=cx.providers.CartoDB.Positron)
# cx.add_basemap(ax, crs=gdf_morocco_boundary.crs, source=cx.providers.OpenStreetMap.HOT)
plt.title('Hydrogen potential map of Morocco', fontsize = 15)
plt.axis('off')
cbar_ax = fig.axes[-1]
cbar_ax.tick_params(labelsize=12)
cbar_ax.yaxis.label.set_size(12)
# plt.savefig("Maps/mca_morocco_2050.pdf", format="pdf", dpi=300)
plt.show()

    #Diffs
gdf_mca_morocco_diff = gpd.GeoDataFrame(geometry=gdf_mca_morocco_2025.geometry, crs = gdf_mca_morocco_2025.crs,
                                               data = gdf_mca_morocco_2050['Hydrogen_potential'] - gdf_mca_morocco_2025['Hydrogen_potential'])

cmap = plt.get_cmap(theme_diff)
vals = np.linspace(0, 1, cmap.N)
colors = cmap(vals)
alpha = np.where(vals > 0.99, 0, 1)
colors[:, -1] = alpha
transparent_cmap = mcolors.ListedColormap(colors)

# Map MCA diff
fig, ax = plt.subplots(figsize=(15, 10))
gdf_morocco_boundary.plot(ax=ax, edgecolor='black', facecolor="none", linewidth=1)
gdf_mca_morocco_diff.plot(ax=ax,vmax = 0, cmap = transparent_cmap, column= 0, legend=True, legend_kwds={"label": "Relativ change in hydrogen potential", "orientation": "vertical"})
cx.add_basemap(ax, crs=gdf_mca_morocco_2025.crs, source=cx.providers.CartoDB.Positron)
plt.title('Change in hydrogen potential of Morocco', fontsize = 15)
plt.axis('off')
cbar_ax = fig.axes[-1]
cbar_ax.tick_params(labelsize=12)
cbar_ax.yaxis.label.set_size(12)
# plt.savefig("Maps/mca_morocco_diff.pdf", format="pdf", dpi=300)
plt.show()