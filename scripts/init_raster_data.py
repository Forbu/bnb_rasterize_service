import rasterio
import numpy as np
import geopandas as gpd

from rasterio.windows import Window
from shapely.geometry import MultiPoint

from bnbserver.extracts_functions import get_raster_value

# import logger
from bnbserver.logger import logger

# init logger
logger = logger()

logger.info("Beginning computing all the points to create tiles")

# read france shapefile in data/regions_2015_metropole_region.shp
data = gpd.read_file("/home/data/regions_2015_metropole_region.json")

# change crs to 2154
data = data.to_crs("EPSG:2154")

# we create a raster file for each 1km2 tile for the whole france (EPSG:2154)
# first we get the limits of the france shapefile
xmin, ymin, xmax, ymax = data.total_bounds

#### 1. We get a list of point that are inside the polygon
point_list = []
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

    point_list.append(result)

# now we flatten the list
point_list = [item for sublist in point_list for item in sublist]

logger.info("Computing all the points to create tiles done")

logger.info("Beginning computing all the points to create tiles")

step = 5
height_tot = int((ymax - ymin) / step)
width_tot = int((xmax - xmin) / step)

info_to_extract = "igntop202103_bat_hauteur"
file_name = '/home/data/france_buildingh.tif'

profile = {'driver': 'GTiff', 'height': height_tot, 'width': width_tot, 'count': 1, 'dtype': rasterio.float16}

with rasterio.open(file_name, 'w', crs='EPSG:2154', **profile) as dst:

    # we loop over all the points information and then we use get_raster_value to get the value of the raster at the point
    # we write the value in the raster file using the window
    for index, row in point_list.iterrows():

        # get the value of the raster at the point
        value = get_raster_value(row['geometry'].x, row['geometry'].y, info_to_extract)

        # the beginning is at row['geometry'].x - 500 and row['geometry'].y - 500
        # the end is at row['geometry'].x + 500 and row['geometry'].y + 500
        # get the window
        window = Window.from_slices(((row['geometry'].y - 500)/step, (row['geometry'].y + 500)/step), ((row['geometry'].x - 500)/step, (row['geometry'].x + 500)/step))

        # write the value in the raster file
        dst.write(value, window=window)


logger.info("Computing all the points to create tiles done")

