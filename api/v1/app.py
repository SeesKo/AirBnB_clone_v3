#!/usr/bin/python3
"""
Creates and runs a Flask web application for a RESTful API.
"""
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {'origins': ['0.0.0.0']}})


@app.errorhandler(404)
def not_found(error):
    """Return a JSON-formatted 404 response"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def close_storage(exception):
    """Closes storage when app context is torn down"""
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", "5000"))
    app.run(host=host, port=port, threaded=True)
