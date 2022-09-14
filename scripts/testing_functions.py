import rasterio
from rasterio.plot import show
from rasterio.plot import show_hist
from rasterio.mask import mask

## ici on lit les données de la carte de la France dans le repertoire data/bnb_export.gpkg
import fiona
import pprint

from osgeo import gdal


import time

start_time = time.time()

X, Y = 648731.0, 6858949.0


with fiona.open("/home/data/bnb_export.gpkg/bnb_export.gpkg") as fiona_collection:
    
    vector_data = fiona_collection.filter(bbox=(X, Y, X + 1000, Y + 1000))
    vector_data = list(vector_data)

vector_data_shape = []

# we go through the generator and change the geometry type to polygon
for element in vector_data: 

    height = element["properties"]['igntop202103_bat_hauteur'] 

    if height == None:
        height = -1

    vector_data_shape.append((element["geometry"], float(height)))

    print(element["properties"]['igntop202103_bat_hauteur'])


pprint.pprint(vector_data_shape[33])

data_raster = rasterio.features.rasterize(vector_data_shape, out_shape=(200, 200), fill=0, dtype='float32', all_touched=True, default_value=1)

# plot data_raster and save it with matplotlib
import matplotlib.pyplot as plt
plt.imshow(data_raster)
plt.savefig('/home/data_raster.png')


print(data_raster)

# print max and min value of data_raster
print(data_raster.max())
print(data_raster.min())


print("--- %s seconds ---" % (time.time() - start_time))
print("end")