#!/usr/bin/python3
"""
RESTful endpoints for handling the link
between 'Place' and 'Amenity' objects.
"""
from flask import jsonify, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """Returns the list of all Amenity objects for a given Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, "Place not found")
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes the link between a Place and an Amenity"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, "Place not found")
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None or amenity not in place.amenities:
        abort(404, "Amenity not linked to the Place")
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """Links an Amenity to a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, "Place not found")
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None or amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
