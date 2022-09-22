import pytest
import numpy as np
import geopandas as gpd

from shapely.geometry import Point, Polygon, MultiPolygon

from bnbserver.extracts_functions import get_raster_value
from bnbserver.server import app, create_app

import flask

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # setup app in local mode
    app.config["LOCAL"] = True

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_request_example(client):
    response = client.get("/api/v1/resources/extracts?X=648731.0&Y=6858949.0&distance=500&feature=igntop202103_bat_hauteur")

    print(response.data)

    assert response.status_code == 200

def test_request_example_download(client):
    response = client.get("/api/v1/resources/download?X=648731.0&Y=6858949.0&distance=500&feature=igntop202103_bat_hauteur")

    # we write the file
    with open("test.npy", "wb") as f:
        f.write(response.data)

    # now we read the file
    data = np.load("test.npy")

    print(data)

    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == "attachment; filename=X_648731.0_Y_6858949.0_distance_500_feature_igntop202103_bat_hauteur.npy"