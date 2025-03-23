import numpy as np
import pandas as pd
import geopandas as gpd

#Weights

dict_weights = {'distance': 1/3, 
                'groundwater': 1/3, 
                'EE': 1/3}