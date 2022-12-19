"""
In this script we will create a server that will listen for incoming connections
and create a webapi that will allow us to retrieve the data from the database

The data is stored in a geopackage file and the api will be a REST api with 4 parameters:
X, Y, distance and feature

X, Y are the coordinates of the center of the bbox we want to extract
distance is the distance from the center of the bbox to the edge of the bbox
feature is the feature we want to extract
"""
import os
import flask
from flask import request, send_from_directory

from bnbserver import extracts_functions

import numpy as np


# init the flask app
app = flask.Flask(__name__)


# we create a route that will listen for incoming connections 
@app.route('/api/v1/resources/extracts', methods=['GET'])
def api_extract():
    """
    This function will extract the data from the geopackage file
    Basically it will create a bbox from the parameters and then extract the data from the geopackage file
    """
    # retrieve the parameters from the request
    X = request.args.get('X')
    Y = request.args.get('Y')
    distance = request.args.get('distance')
    feature = request.args.get('feature')

    # we check if the parameters are not None
    if X is None or Y is None or distance is None or feature is None:
        return "Error: Missing parameters"
 
    # convert the parameters to float
    X = float(X)
    Y = float(Y)
    distance = int(distance)

    # call the function that will extract the data
    raster_value = extracts_functions.get_raster_value(X, Y, distance, feature)

    # return the array as a json
    return flask.jsonify(raster_value.values.tolist())

# download the data from raster data (faster than the api)
@app.route('/api/v1/resources/download', methods=['GET'])
def api_download():
    """
    Direct download of the data from the raster data
    """
    # retrieve the parameters from the request
    X = request.args.get('X')
    Y = request.args.get('Y')
    distance = request.args.get('distance')
    feature = request.args.get('feature')

    # we check if the parameters are not None
    if X is None or Y is None or distance is None or feature is None:
        return "Error: Missing parameters"

    # convert the parameters to float
    X = float(X)
    Y = float(Y)
    distance = int(distance)
    
    # call the function that will extract the data
    raster_value = extracts_functions.get_raster_value(X, Y, distance, feature)

    # create the filename
    filename = "X_" + str(X) + "_Y_" + str(Y) + "_distance_" + str(distance) + "_feature_" + str(feature) + ".npy"

    # save the array as a numpy file
    np.save(filename, raster_value)

    # return the file
    return send_from_directory(os.getcwd(), filename, as_attachment=True)

def create_app():
    return app

# launch the server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
