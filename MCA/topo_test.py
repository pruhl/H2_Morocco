import rasterio

with rasterio.open(r"C:\Users\psclr\Documents\02 Master\Masterprojekt\QGIS\Daten\topo MA.tif") as src:
    # Read the data from the first band
    data = src.read()
    
    # Get the metadata
    metadata = src.meta