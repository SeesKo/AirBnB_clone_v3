#!/usr/bin/python3
"""
API endpoints for managing 'Amenity' objects in a RESTful manner.
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"],
                 strict_slashes=False)
def get_amenities():
    """Returns a list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Returns an Amenity object by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404, "Amenity not found")
    return jsonify(amenity.to_dict())


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def create_amenity():
    """Creates a new Amenity object"""
    amenity_data = request.get_json()
    if amenity_data is None:
        abort(400, "Not a JSON")
    if "name" not in amenity_data:
        abort(400, "Missing name")

    new_amenity = Amenity(name=amenity_data["name"])
    storage.new(new_amenity)
    storage.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity object by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404, "Amenity not found")

    storage.delete(amenity)
    storage.save()

    return jsonify({}), 200


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an Amenity object by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404, "Amenity not found")

    amenity_data = request.get_json()
    if amenity_data is None:
        abort(400, "Not a JSON")

    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in amenity_data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)

    storage.save()
    return jsonify(amenity.to_dict()), 200
