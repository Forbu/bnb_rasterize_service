import rasterio
from rasterio.plot import show
from rasterio.plot import show_hist
from rasterio.mask import mask

## ici on lit les données de la carte de la France dans le repertoire data/bnb_export.gpkg
import fiona
import pprint

from osgeo import gdal
from osgeo import gdal
from osgeo import ogr
from osgeo import gdalconst

import time

import geopandas as gpd

from shapely.geometry import Point, Polygon, MultiPolygon

start_time = time.time()

X, Y = 648731.0, 6858949.0

file_path_gpkg = "/home/data/bnb_export.gpkg"

# start timer 
start_time = time.time()

with fiona.open(file_path_gpkg) as fiona_collection:
    
    vector_data = fiona_collection.filter(bbox=(X, Y, X + 1000, Y + 1000))
    vector_data = list(vector_data)

    print(fiona_collection.crs)

vector_data_shape = []
geometries = []
heights = []

# we go through the generator and change the geometry type to polygon
for element in vector_data: 

    print(element["properties"].keys())

    try:

        height = element["properties"]['igntop202103_bat_hauteur'] 

        if height == None:
            height = -1

        vector_data_shape.append((element["geometry"], float(height)))

        # create the multipolygon and append it to the geometries list
        geometries.append(MultiPolygon([Polygon(element["geometry"]["coordinates"][0][0])]))
        
        # append the height to the heights list
        heights.append(float(height))
    except:
        pass

# now we use put the shapes in a geopandas dataframe
gdf = gpd.GeoDataFrame(heights, geometry=geometries, columns=['height'])

# limit the geomatries to the ones that are included in the bbox (X, Y, X + 1000, Y + 1000)
# now we rasterize the dataframe using geocube
from geocube.api.core import make_geocube

geom = {
    "type": "Polygon", 
    "coordinates": [
        [
            [X, Y], [X, Y + 1000], [X + 1000, Y + 1000], [X + 1000, Y], [X, Y]
        ]
    ],
    "crs": {"properties": {"name": "EPSG:2154"}}
}

print(gdf)

print(type(gdf))

gdf.crs = {'init': 'epsg:2154'}

gdf = gdf.to_crs(2154)
#gdf = gdf.set_crs("EPSG:2154")

cube = make_geocube(vector_data=gdf, measurements=['height'], resolution=(5, -5), geom=geom, fill=0)

# transform the cube to a numpy array
cube_array = cube.to_array()

print(cube_array)

# print timer end
print("--- %s seconds ---" % (time.time() - start_time))