"""
In this script we will create a server that will listen for incoming connections
and create a webapi that will allow us to retrieve the data from the database

The data is stored in a geopackage file and the api will be a REST api with 4 parameters:
X, Y, distance and feature

X, Y are the coordinates of the center of the bbox we want to extract
distance is the distance from the center of the bbox to the edge of the bbox
feature is the feature we want to extract
"""

import flask
from flask import request, send_from_directory

from bnbserver import extracts_functions

import numpy as np
import os

# init the flask app
app = flask.Flask(__name__)


# we create a route that will listen for incoming connections 
@app.route('/api/v1/resources/extracts', methods=['GET'])
def api_extract():
    # retrieve the parameters from the request
    X = request.args.get('X')
    Y = request.args.get('Y')
    distance = request.args.get('distance')
    feature = request.args.get('feature')

    # we check if the parameters are not None
    if X is None or Y is None or distance is None or feature is None:
        return "Error: Missing parameters"
    
    # call the function that will extract the data
    raster_value = extracts_functions.get_raster_value(X, Y, distance, feature)

    # return the array as a json
    return flask.jsonify(raster_value.tolist())

# launch the server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
