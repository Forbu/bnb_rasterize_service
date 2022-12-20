import pytest
import numpy as np
import geopandas as gpd

import os

from shapely.geometry import Point, Polygon, MultiPolygon

import matplotlib.pyplot as plt

from bnbserver.extracts_functions import get_raster_value

from pyproj import Transformer

def test_get_raster_value():
    """
    test that the function return the correct value
    We init X, Y with position of the point corresponding to the middle of paris in EPSG:2154
    """

    X, Y = 989567.339786, 6733416.101491
    distance = 500
    feature = "igntop202103_bat_hauteur"

    raster_value = get_raster_value(X, Y, distance, feature)

    print(raster_value)
    print(raster_value.x)
    print(raster_value.y)

    # now we plot the raster and save it in the folder images
    plt.imshow(raster_value.values[0], origin='lower')

    plt.savefig("images/rasterize_epsg_2154.png")

    assert raster_value.values.shape == (1, 201, 201)

def test_path_row_data():
    """
    test to check if the data (gpkg) is available
    """
    path_gpck = "/home/data/bnb_export.gpkg"

    assert os.path.exists(path_gpck)


def test_rasterize_epsg_27572():
    """
    test to check if the rasterize function work
    """
    X, Y = 989567.339786, 6733416.101491 # coordinates of the center of Paris in EPSG:2154

    # convert the coordinates to EPSG:27572
    transformer = Transformer.from_crs("epsg:2154", "epsg:27572")

    X, Y = transformer.transform(X, Y)

    distance = 500
    feature = "igntop202103_bat_hauteur"

    raster_value = get_raster_value(X, Y, distance, feature, epsg=27572, resolution=5)

    # now we plot the raster and save it in the folder images
    plt.imshow(raster_value.values[0], origin='lower')

    plt.savefig("images/rasterize_epsg_27572_v2.png")

    # now we do the same thing but with the coordinates in EPSG:2154 (we transform the coordinates)
    transformer = Transformer.from_crs("epsg:27572", "epsg:2154")

    X, Y = transformer.transform(X, Y)

    raster_value = get_raster_value(X, Y, distance, feature, epsg=2154, resolution=5)

    # now we plot the raster and save it in the folder images
    plt.imshow(raster_value.values[0], origin='lower')

    plt.savefig("images/rasterize_epsg_2154_v2.png")

    assert raster_value.values.shape == (1, 201, 201)
    assert False