import geopandas as gpd

# Data
    # Current potential
gdf_grid = gpd.read_file('Grid_morocco/grid_morocco_clear.shp')
    # Wind
    # Source: Global Wind Atlas
gdf_wind_morocco_utm29n = gpd.read_file('Data\Wind_Energiedichte\wind_yeald\Wind_pot_morocco_FLH.shp').to_crs("EPSG:32629")

# Spatial join: alle Wind-Geometrien auf die Grid-Zellen mappen
joined = gpd.sjoin(gdf_grid,
                   gdf_wind_morocco_utm29n[['FLH_wind', 'geometry']],
                   how='left',
                   predicate='intersects')

# Durchschnitt pro Zelle berechnen
df_mean = joined.groupby(joined.index)['FLH_wind'].mean()
df_mean = df_mean.fillna(0)

# CSV
df_mean.to_csv('results/results_wind_flh.csv', index=False)