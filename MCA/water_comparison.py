import geopandas as gpd
import matplotlib.pyplot as plt

#####
#RdYlGn gdf_water_50_50['sum'].max() turbo_r turbo
#####

# Wateravailable
    #2025
gdf_water_available     = gpd.read_file('Maps/mca_h2_morocco_2025_water_available.shp')     #V1
gdf_water_available_V2  = gpd.read_file('Maps/mca_h2_morocco_2025_water_available_V2.shp')  #V2
gdf_water_available_V3  = gpd.read_file('Maps/mca_h2_morocco_2025_water_available_V3.shp')  #V3
    #2050
gdf_water_available_2050     = gpd.read_file('Maps/mca_h2_morocco_2050_water_available_V1.shp')  #V1
gdf_water_available_2050_V2  = gpd.read_file('Maps/mca_h2_morocco_2050_water_available_V2.shp')  #V2
gdf_water_available_2050_V3  = gpd.read_file('Maps/mca_h2_morocco_2050_water_available_V3.shp')  #V3
    #Diffs
gdf_water_available_diff_V1 = gpd.GeoDataFrame(geometry=gdf_water_available.geometry, crs = gdf_water_available.crs,
                                               data = gdf_water_available_2050['sum'] - gdf_water_available['sum'])

gdf_water_available_diff_V2 = gpd.GeoDataFrame(geometry=gdf_water_available.geometry, crs = gdf_water_available.crs,
                                               data = gdf_water_available_2050_V2['sum'] - gdf_water_available_V2['sum'])

gdf_water_available_diff_V3 = gpd.GeoDataFrame(geometry=gdf_water_available.geometry, crs = gdf_water_available.crs,
                                               data = gdf_water_available_2050_V3['sum'] - gdf_water_available_V3['sum'])

# 50/50 Water/Res
    #2025
gdf_water_50_50         = gpd.read_file('Maps/mca_h2_morocco_2025_water_50_50.shp')     #V1
gdf_water_50_50_V2      = gpd.read_file('Maps/mca_h2_morocco_2025_water_50_50_V2.shp')  #V2
gdf_water_50_50_V3      = gpd.read_file('Maps/mca_h2_morocco_2025_water_50_50_V3.shp')  #V3
    #2050
gdf_water_50_50_2050    = gpd.read_file('Maps/mca_h2_morocco_2050_water_50_50.shp')     #V1
gdf_water_50_50_2050_V2 = gpd.read_file('Maps/mca_h2_morocco_2050_water_50_50_V2.shp')  #V2
gdf_water_50_50_2050_V3 = gpd.read_file('Maps/mca_h2_morocco_2050_water_50_50_V3.shp')  #V3
    #Diffs
gdf_water_50_50_diff_V1 = gpd.GeoDataFrame(geometry=gdf_water_available.geometry, crs = gdf_water_available.crs,
                                               data = gdf_water_50_50_2050['sum'] - gdf_water_50_50['sum'])

gdf_water_50_50_diff_V2 = gpd.GeoDataFrame(geometry=gdf_water_available.geometry, crs = gdf_water_available.crs,
                                               data = gdf_water_50_50_2050_V2['sum'] - gdf_water_50_50_V2['sum'])

gdf_water_50_50_diff_V3 = gpd.GeoDataFrame(geometry=gdf_water_available.geometry, crs = gdf_water_available.crs,
                                               data = gdf_water_50_50_2050_V3['sum'] - gdf_water_50_50_V3['sum'])

# Water res
    #2025
gdf_water_res           = gpd.read_file('Maps/mca_h2_morocco_2025_water_res.shp')       #V1
gdf_water_res_V2        = gpd.read_file('Maps/mca_h2_morocco_2025_water_res_V2.shp')    #V2
gdf_water_res_V3        = gpd.read_file('Maps/mca_h2_morocco_2025_water_res_V3.shp')    #V3
    #2050
gdf_water_res_2050      = gpd.read_file('Maps/mca_h2_morocco_2050_water_res_V1.shp')    #V1
gdf_water_res_2050_V2   = gpd.read_file('Maps/mca_h2_morocco_2050_water_res_V2.shp')    #V2
gdf_water_res_2050_V3   = gpd.read_file('Maps/mca_h2_morocco_2050_water_res_V3.shp')    #V2
    #Diffs
gdf_water_res_diff_V1 = gpd.GeoDataFrame(geometry=gdf_water_available.geometry, crs = gdf_water_available.crs,
                                               data = gdf_water_res_2050['sum'] - gdf_water_res['sum'])

gdf_water_res_diff_V2 = gpd.GeoDataFrame(geometry=gdf_water_available.geometry, crs = gdf_water_available.crs,
                                               data = gdf_water_res_2050_V2['sum'] - gdf_water_res_V2['sum'])

gdf_water_res_diff_V3 = gpd.GeoDataFrame(geometry=gdf_water_available.geometry, crs = gdf_water_available.crs,
                                               data = gdf_water_res_2050_V3['sum'] - gdf_water_res_V3['sum'])

# # CWB
# gdf_cwb_2050            = gpd.read_file('Data/cwp_2050.shp')

# # Plots for determining which water analysis is performed
# fig, axs = plt.subplots(1, 3, figsize = (15,5))
# fig.suptitle('Comparison of the water analysis for Morocco in 2025')
# gdf_water_res.plot(column='sum', cmap = 'turbo_r', legend = False, vmin=0, vmax=gdf_water_res['sum'].max(), ax = axs[0])
# axs[0].set_title('Residual water availability')

# gdf_water_50_50.plot(column='sum', cmap = 'turbo_r', legend = False, vmin=0, vmax=gdf_water_50_50['sum'].max(), ax = axs[1])
# axs[1].set_title('Residual and water availability 50/50')

# gdf_water_available.plot(column='sum', cmap = 'turbo_r', legend = False, vmin=0, vmax=gdf_water_available['sum'].max(), ax = axs[2])
# axs[2].set_title('Water availability')

# Plots with 50/50 rating of water residual and water availability V1
    #Water 50/50
fig, axs = plt.subplots(3, 3, figsize = (15,15))
fig.suptitle('Wateranalysis (50/50 rating)')
gdf_water_50_50.plot(column='sum', cmap = 'turbo_r', legend = True, vmin=0, vmax=gdf_water_50_50['sum'].max(), ax = axs[0, 0])
axs[0, 0].set_title('V1 2025')

gdf_water_50_50_2050.plot(column='sum', cmap = 'turbo_r', legend = True, vmin=0, vmax=gdf_water_50_50['sum'].max(), ax = axs[1, 0])
axs[1, 0].set_title('V1 2050')

gdf_water_50_50_diff_V1.plot(column='sum', cmap = 'Blues_r', legend = True, ax = axs[2, 0])
axs[2, 0].set_title('V1 Diff')

gdf_water_50_50_V2.plot(column='sum', cmap = 'turbo_r', legend = True, vmin=0, vmax=gdf_water_50_50_V2['sum'].max(), ax = axs[0, 1])
axs[0, 1].set_title('V2 2025')

gdf_water_50_50_2050_V2.plot(column='sum', cmap = 'turbo_r', legend = True, vmin=0, vmax=gdf_water_50_50_V2['sum'].max(), ax = axs[1, 1])
axs[1, 1].set_title('V2 2050')

gdf_water_50_50_diff_V2.plot(column='sum', cmap = 'Blues_r', legend = True, ax = axs[2, 1])
axs[2, 1].set_title('V2 Diff')

gdf_water_50_50_V3.plot(column='sum', cmap = 'turbo_r', legend = True, vmin=0, vmax=gdf_water_50_50_V3['sum'].max(), ax = axs[0, 2])
axs[0, 2].set_title('V3 2025')

gdf_water_50_50_2050_V3.plot(column='sum', cmap = 'turbo_r', legend = True, vmin=0, vmax=gdf_water_50_50_2050_V3['sum'].max(), ax = axs[1, 2])
axs[1, 2].set_title('V3 2050')

gdf_water_50_50_diff_V3.plot(column='sum', cmap = 'Blues_r', legend = True, ax = axs[2, 2])
axs[2, 2].set_title('V3 Diff')

    #Water availability
fig, axs = plt.subplots(3, 3, figsize = (15,15))
fig.suptitle('Wateranalysis (Availability)')
gdf_water_available.plot(column='sum', cmap = 'turbo_r', legend = True, vmin=0, vmax=gdf_water_available['sum'].max(), ax = axs[0, 0])
axs[0, 0].set_title('V1 2025')

gdf_water_available_2050.plot(column='sum', cmap = 'turbo_r', legend = True, vmin=0, vmax=gdf_water_available['sum'].max(), ax = axs[1, 0])
axs[1, 0].set_title('V1 2050')

gdf_water_available_diff_V1.plot(column='sum', cmap = 'Blues_r', legend = True, ax = axs[2, 0])
axs[2, 0].set_title('V1 Diff')

gdf_water_available_V2.plot(column='sum', cmap = 'turbo_r', legend = True, vmin=0, vmax=gdf_water_available_V2['sum'].max(), ax = axs[0, 1])
axs[0, 1].set_title('V2 2025')

gdf_water_available_2050_V2.plot(column='sum', cmap = 'turbo_r', legend = True, vmin=0, vmax=gdf_water_available_V2['sum'].max(), ax = axs[1, 1])
axs[1, 1].set_title('V2 2050')

gdf_water_available_diff_V2.plot(column='sum', cmap = 'Blues_r', legend = True, ax = axs[2, 1])
axs[2, 1].set_title('V2 Diff')

gdf_water_available_V3.plot(column='sum', cmap = 'turbo_r', legend = True, vmin=0, vmax=gdf_water_available_V3['sum'].max(), ax = axs[0, 2])
axs[0, 2].set_title('V3 2025')

gdf_water_available_2050_V3.plot(column='sum', cmap = 'turbo_r', legend = True, vmin=0, vmax=gdf_water_available_V3['sum'].max(), ax = axs[1, 2])
axs[1, 2].set_title('V3 2050')

gdf_water_available_diff_V3.plot(column='sum', cmap = 'Blues_r', legend = True, ax = axs[2, 2])
axs[2, 2].set_title('V3 Diff')

    # Water residual
fig, axs = plt.subplots(3, 3, figsize = (15,15))
fig.suptitle('Wateranalysis (Residual)')
gdf_water_res.plot(column='sum', cmap = 'turbo_r', legend = True, vmin=0, vmax=gdf_water_res['sum'].max(), ax = axs[0, 0])
axs[0, 0].set_title('V1 2025')

gdf_water_res_2050.plot(column='sum', cmap = 'turbo_r', legend = True, vmin=0, vmax=gdf_water_res['sum'].max(), ax = axs[1, 0])
axs[1, 0].set_title('V1 2050')

gdf_water_res_diff_V1.plot(column='sum', cmap = 'Blues_r', legend = True, ax = axs[2, 0])
axs[2, 0].set_title('V1 Diff')

gdf_water_res_V2.plot(column='sum', cmap = 'turbo_r', legend = True, vmin=0, vmax=gdf_water_res_V2['sum'].max(), ax = axs[0, 1])
axs[0, 1].set_title('V2 2025')

gdf_water_res_2050_V2.plot(column='sum', cmap = 'turbo_r', legend = True, vmin=0, vmax=gdf_water_res_V2['sum'].max(), ax = axs[1, 1])
axs[1, 1].set_title('V2 2050')

gdf_water_res_diff_V2.plot(column='sum', cmap = 'Blues_r', legend = True, ax = axs[2, 1])
axs[2, 1].set_title('V2 Diff')

gdf_water_res_V3.plot(column='sum', cmap = 'turbo_r', legend = True, vmin=0, vmax=gdf_water_res_V3['sum'].max(), ax = axs[0, 2])
axs[0, 2].set_title('V3 2025')

gdf_water_res_2050_V3.plot(column='sum', cmap = 'turbo_r', legend = True, vmin=0, vmax=gdf_water_res_V3['sum'].max(), ax = axs[1, 2])
axs[1, 2].set_title('V3 2050')

gdf_water_res_diff_V3.plot(column='sum', cmap = 'Blues_r', legend = True, ax = axs[2, 2])
axs[2, 2].set_title('V3 Diff')

# #CWB
# gdf_cwb_2050.plot(column='CWB', cmap = 'Blues', legend=True)