#!/usr/bin/python3
"""
API endpoints for managing 'City' objects in a RESTful manner.
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_cities(state_id):
    """Returns a list of all City objects for a given State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404, "State not found")
    cities = state.cities  # Get all cities for this State
    return jsonify([city.to_dict() for city in cities])


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def get_city(city_id):
    """Returns a City object by ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404, "City not found")
    return jsonify(city.to_dict())


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a new City object for a given State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404, "State not found")

    city_data = request.get_json()
    if city_data is None:
        abort(400, "Not a JSON")

    if "name" not in city_data:
        abort(400, "Missing name")

    new_city = City(name=city_data["name"], state_id=state.id)
    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object by ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404, "City not found")

    storage.delete(city)
    storage.save()

    return jsonify({}), 200


@app_views.route("/cities/<city_id>", methods=["PUT"],
                 strict_slashes=False)
def update_city(city_id):
    """Updates a City object by ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404, "City not found")

    city_data = request.get_json()
    if city_data is None:
        abort(400, "Not a JSON")

    ignore_keys = ["id", "state_id", "created_at", "updated_at"]
    for key, value in city_data.items():
        if key not in ignore_keys:
            setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict()), 200
