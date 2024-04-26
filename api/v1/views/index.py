#!/usr/bin/python3
"""
Module defines API endpoints for checking the API
status and retrieving object type statistics.
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def get_status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def get_stats():
    """Returns the count of each object type"""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }
    return jsonify(stats)
