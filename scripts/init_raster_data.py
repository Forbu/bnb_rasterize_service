import rasterio
import numpy as np
import geopandas as gpd

from rasterio.windows import Window
from shapely.geometry import MultiPoint
import json

import random


import os, sys
# get parent of __file__
file_path = "/".join(os.path.realpath(__file__).split("/")[:-1])
print(file_path)
sys.path.append(os.path.dirname(file_path))


from bnbserver.extracts_functions import get_raster_value

# import logger from logging package
from logging import getLogger

# init logger
logger = getLogger(__name__)

logger.info("Beginning computing all the points to create tiles")

# read france shapefile in data/regions_2015_metropole_region.shp
data = gpd.read_file("/home/data/regions_2015_metropole_region.json")

# change crs to 2154
data = data.to_crs("EPSG:2154")

# we create a raster file for each 1km2 tile for the whole france (EPSG:2154)
# first we get the limits of the france shapefile
xmin_global, ymin_global, xmax_global, ymax_global = data.total_bounds

#### 1. We get a list of point that are inside the polygon
point_list = []
for index, row in data.iterrows():

    # first we the bound of the polygon
    bbox = row['geometry'].bounds 

    xmin, ymin, xmax, ymax = row['geometry'].bounds
    
    # now we create the 1km2 tiles
    x = np.arange(np.floor(xmin), np.ceil(xmax) + 1, step=1000)  # array([0., 1., 2.])
    y = np.arange(np.floor(ymin), np.ceil(ymax) + 1, step=1000)  # array([0., 1., 2.])

    points = MultiPoint(np.transpose([np.tile(x, len(y)), np.repeat(y, len(x))]))

    # now we get all the tiles that are inside the polygon
    result = points.intersection(row['geometry'])

    point_list.append(result)

# now we flatten the list
point_list = [item for sublist in point_list for item in sublist]

# little shuffle
random.shuffle(point_list)

logger.info("Computing all the points to create tiles done")

logger.info("Beginning computing all the points to create tiles")

step = 5
height_tot = int((ymax_global - ymin_global) / step)
width_tot = int((xmax_global - xmin_global) / step)

info_to_extract = "igntop202103_bat_hauteur"
file_name = '/home/data/france_buildingh.tif'

profile = {'driver': 'GTiff', 'height': height_tot, 'width': width_tot, 'count': 1, 'dtype': rasterio.int8, 'crs': 'EPSG:2154'}

distance = 500

# we create a Affine transform that map xmin to 0 and ymin to 0 and ymax to height_tot and xmax to width_tot
transform = rasterio.transform.from_bounds(xmin, ymin, xmax, ymax, width_tot, height_tot) 

# save projection
projection = {"ymin_global": ymin_global, "xmin_global": xmin_global, "ymax_global": ymax_global, "xmax_global": xmax_global, "step": step}

# save projection as json
with open('/home/data/france_projection.json', 'w') as outfile:
    json.dump(projection, outfile)

with rasterio.open(file_name, 'w', **profile) as dst:

    # we loop over all the points information and then we use get_raster_value to get the value of the raster at the point
    # we write the value in the raster file using the window
    for index, row in enumerate(point_list):


        # get the value of the raster at the point
        value = get_raster_value(row.x, row.y, distance, feature_name=info_to_extract)

        value  = value.values[0, 1:201, 0:200]


        slice_y = (int((row.y - distance - ymin_global)/step), int((row.y + distance - ymin_global)/step))
        slice_x = (int((row.x - distance - xmin_global)/step), int((row.x + distance - xmin_global)/step))


        # we transform the two slice
        window = Window.from_slices(slice_y, slice_x)

        # write the value in the raster file
        dst.write(value, window=window, indexes=1)

        break


logger.info("Computing all the points to create tiles done")

