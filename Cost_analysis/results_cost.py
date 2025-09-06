import geopandas as gpd
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import contextily as cx

# Comparison of ports in 2025 and 2050
gdf_morocco_boundary    = gpd.read_file(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\morocco_Morocco_Country_Boundary.shp").to_crs("EPSG:32629")
gdf_ports_2025 = gpd.read_file('Data/industrial_ports_morocco_2025.shp').to_crs("EPSG:32629")
gdf_ports_2050 = gpd.read_file('Data/industrial_ports_morocco_2050.shp').to_crs("EPSG:32629")
ports_2025 = set(gdf_ports_2025['name'])
ports_2050 = set(gdf_ports_2050['name'])
new_ports = ports_2050 - ports_2025
gdf_ports_new = gdf_ports_2050[gdf_ports_2050['name'].isin(new_ports)]

fig, ax = plt.subplots(figsize=(10, 10))
# Für jeden Punkt Namen als Text hinzufügen
y_offset = 10000
x_offset = -20000
for idx, row in gdf_ports_2050.iterrows():
    x = row.geometry.x  # x-Koordinate
    y = row.geometry.y  # y-Koordinate
    name = row['name']  # Name aus Spalte 'name'
    if name in new_ports:
        if name == 'Mohammedia':
            ax.text(x + x_offset, y + y_offset*3, name, fontsize=10, color='red', 
                    ha='right', va='bottom')
        else:
            ax.text(x + x_offset, y + y_offset, name, fontsize=10, color='red', 
                ha='right', va='bottom')
    else:
        if name in ['Tanger Med', 'Tanger Ville']:
            if name == 'Tanger Med':
                ax.text(x + x_offset, y + y_offset, 'Tanger', fontsize=10, color='blue', 
                    ha='right', va='bottom')
        else:
            ax.text(x + x_offset, y + y_offset, name, fontsize=10, color='blue', 
                ha='right', va='bottom')
gdf_morocco_boundary.plot(ax=ax, edgecolor='black', facecolor="none", linewidth=2)
gdf_ports_2025.plot(ax=ax, color='blue', marker='o', markersize=50, label='Current Ports Morocco')
gdf_ports_new.plot(ax=ax, color='red', marker='o', markersize=50, label='New Ports Morocco')
cx.add_basemap(ax, crs=gdf_morocco_boundary.crs, source=cx.providers.CartoDB.Positron)
# cx.add_basemap(ax, crs=gdf_morocco_boundary.crs, source=cx.providers.OpenStreetMap.HOT)
plt.title('Ports of Morocco for energy trafic and industrial applications', fontsize = 15)
plt.legend(loc='upper left', fontsize=12)
plt.axis('off')
plt.savefig("ports_morocco.svg", format="svg", dpi=300)
plt.show()