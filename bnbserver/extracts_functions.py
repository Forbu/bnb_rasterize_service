import fiona
import numpy as np

from osgeo import gdal
from osgeo import gdal
from osgeo import ogr
from osgeo import gdalconst

import geopandas as gpd
from geocube.api.core import make_geocube

from shapely.geometry import Point, Polygon, MultiPolygon

path_gpck = "/home/data/bnb_export.gpkg/bnb_export.gpkg"

# function that take as input a position X, Y, distance and the feature we want to retrieve and return the raster value at this position 
def get_raster_value(X, Y, distance, feature_name="igntop202103_bat_hauteur"):
    """
    parameters:
        X, Y: position of the point
        distance: distance to the point
        feature: feature we want to retrieve

    return:
        raster_value: raster value at the position X, Y (array)
    """

    # first we create the bbox supposing X, Y is the center of the bbox
    bbox = (X - distance, Y - distance, X + distance, Y + distance)

    # we open the gpck file and filter the data using the bbox
    with fiona.open(path_gpck) as fiona_collection:
        
        vector_data = fiona_collection.filter(bbox=bbox)
        vector_data = list(vector_data)

    # now create the geometries and the heights list
    geometries = []
    feature = []

    # we go through the generator and change the geometry type to polygon
    for element in vector_data: 

        feature_value = element["properties"][feature_name]

        if feature_value == None:
            feature_value = -1

        # create the multipolygon and append it to the geometries list
        geometries.append(MultiPolygon([Polygon(element["geometry"]["coordinates"][0][0])]))
        
        # append the height to the heights list
        feature.append(float(feature_value))

    # now we use put the shapes in a geopandas dataframe
    gdf = gpd.GeoDataFrame(feature, geometry=geometries, columns=[feature_name])

    gdf.crs = {'init': 'epsg:2154'}
    gdf = gdf.to_crs(2154)

    # limit the geomatries to the ones that are included in the bbox (X - distance, Y - distance, X + distance, Y + distance)
    geom = {
        "type": "Polygon", 
        "coordinates": [
            [
                [X - distance, Y - distance], [X - distance, Y + distance], [X + distance, Y + distance], [X + distance, Y - distance], [X - distance, Y - distance]
            ]
        ],
        "crs": {"properties": {"name": "EPSG:2154"}}
    }

    # now we rasterize the dataframe using geocube
    cube = make_geocube(
        vector_data=gdf,
        measurements=[feature_name],
        resolution=(5, 5),
        geom=geom,
        fill=0,
    )

    cube_array = cube.to_array()

    return cube_array

# second function to read the raster value at a position X, Y TODO when we will finish the extraction of the data in raster form

