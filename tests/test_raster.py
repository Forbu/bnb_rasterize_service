import pytest
import numpy as np
import geopandas as gpd

from shapely.geometry import Point, Polygon, MultiPolygon

from bnbserver.extracts_functions import get_raster_value

def test_get_raster_value():
    # test that the function return the correct value
    # we init X, Y with position of the point corresponding to the middle of paris in EPSG:2154
    X, Y = 648731.0, 6858949.0
    distance = 500
    feature = "igntop202103_bat_hauteur"

    raster_value = get_raster_value(X, Y, distance, feature)

    print(raster_value)
    print(raster_value.x)
    print(raster_value.y)

    assert raster_value.values.shape == (1, 201, 201)