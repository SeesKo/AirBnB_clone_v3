#!/usr/bin/python3
"""
Creates and runs a Flask web application for a RESTful API.
"""
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    """Closes storage when app context is torn down"""
    storage.close()


if __name__ == "__main__":
    from os import getenv
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", "5000"))
    app.run(host=host, port=port, threaded=True)
