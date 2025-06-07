def list_index(gdf, i, grid):
    cell = grid['geometry'].iloc[i]
    intersects = gdf.intersects(cell)
    return cell, intersects[intersects == True].index.tolist()

def list_index_only_list(cell,gdf):
    intersects = gdf.intersects(cell)
    return intersects[intersects == True].index.tolist()