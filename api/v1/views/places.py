#!/usr/bin/python3
"""
API endpoints for managing 'Place' objects in a RESTful manner.
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places(city_id):
    """Returns a list of all Place objects for a given City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404, "City not found")
    places = city.places
    return jsonify([place.to_dict() for place in places])


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """Returns a Place object by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, "Place not found")
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, "Place not found")

    storage.delete(place)
    storage.save()

    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a new Place for a given City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404, "City not found")

    place_data = request.get_json()
    if place_data is None:
        abort(400, "Not a JSON")

    if "user_id" not in place_data:
        abort(400, "Missing user_id")
    user = storage.get(User, place_data["user_id"])
    if user is None:
        abort(404, "User not found")

    if "name" not in place_data:
        abort(400, "Missing name")

    new_place = Place(
        name=place_data["name"],
        user_id=place_data["user_id"],
        city_id=city_id
    )
    storage.new(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a Place object by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, "Place not found")

    place_data = request.get_json()
    if place_data is None:
        abort(400, "Not a JSON")

    ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in place_data.items():
        if key not in ignore_keys:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/places_search", methods=["POST"],
                 strict_slashes=False)
def search_places():
    """
    Searches for Place objects based on states, cities, or amenities
    """
    request_data = request.get_json()
    if request_data is None:
        abort(400, "Not a JSON")

    state_ids = request_data.get("states", [])
    city_ids = request_data.get("cities", [])
    amenity_ids = request_data.get("amenities", [])

    if not state_ids and not city_ids and not amenity_ids:
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    place_results = set()

    for state_id in state_ids:
        state = storage.get(State, state_id)
        if state is None:
            continue
        for city in state.cities:
            place_results.update(city.places)

    for city_id in city_ids:
        city = storage.get(City, city_id)
        if city is None:
            continue
        place_results.update(city.places)

    if amenity_ids:
        filtered_results = set()
        for place in place_results:
            if all(
                amenity.id in [a.id for a in place.amenities]
                for amenity in amenity_ids
            ):
                filtered_results.add(place)
        place_results = filtered_results

    return jsonify([place.to_dict() for place in place_results])
