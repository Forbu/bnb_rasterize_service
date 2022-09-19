"""
The goal of this script is to create a raster file from a vector file (gpck) using geocube
The main idea of this script is to loop over all the 1km2 tiles and create a raster file for each of them so we can cover all france

"""

import time
import os
import geopandas as gpd

from itertools import product
from shapely.geometry import MultiPoint

import numpy as np

#from bnbserver import extracts_functions

# read france shapefile in data/regions_2015_metropole_region.shp
data = gpd.read_file("/home/data/regions_2015_metropole_region.json")

# change crs to 2154
data = data.to_crs("EPSG:2154")

# we create a raster file for each 1km2 tile for the whole france (EPSG:2154)
# first we get the limits of the france shapefile
xmin, ymin, xmax, ymax = data.total_bounds

print(xmin, ymin, xmax, ymax)



# now for every polygon in the dataframe we wan loop over the 1km2 tiles and create a raster file for each of them
for index, row in data.iterrows():

    print(index)
    print(row)

    # first we the bound of the polygon
    bbox = row['geometry'].bounds 

    xmin, ymin, xmax, ymax = row['geometry'].bounds
    
    # now we create the 1km2 tiles
    x = np.arange(np.floor(xmin), np.ceil(xmax) + 1, step=1000)  # array([0., 1., 2.])
    y = np.arange(np.floor(ymin), np.ceil(ymax) + 1, step=1000)  # array([0., 1., 2.])

    points = MultiPoint(np.transpose([np.tile(x, len(y)), np.repeat(y, len(x))]))

    # now we get all the tiles that are inside the polygon
    result = points.intersection(row['geometry'])






