def list_index(gdf, i, grid):
    cell = grid['geometry'].iloc[i]
    intersects = gdf.intersects(cell)
    return cell, intersects[intersects == True].index.tolist()