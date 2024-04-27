#!/usr/bin/python3
"""
Creates and runs a Flask web application for a RESTful API.
"""
from flask import Flask, jsonify, make_response, Blueprint
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {'origins': ['0.0.0.0']}})


@app.teardown_appcontext
def teardown_appcontext(self):
    """ closes down current session """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """
    a handler for 404 errors that returns a
    JSON-formatted 404 status code response
    """
    return (jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    hosts = getenv("HBNB_API_HOST", default='0.0.0.0')
    ports = int(os.getenv("HBNB_API_PORT", default=5000))
    app.run(host=hosts, port=ports, threaded=True)
