#!/usr/bin/python3
"""
API endpoints for managing 'User' objects in a RESTful manner.
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"],
                 strict_slashes=False)
def get_users():
    """Returns a list of all User objects"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def get_user(user_id):
    """Returns a User object by ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404, "User not found")
    return jsonify(user.to_dict())


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Creates a new User object"""
    user_data = request.get_json()
    if user_data is None:
        abort(400, "Not a JSON")
    if "email" not in user_data:
        abort(400, "Missing email")
    if "password" not in user_data:
        abort(400, "Missing password")

    new_user = User(email=user_data["email"], password=user_data["password"])
    storage.new(new_user)
    storage.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object by ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404, "User not found")

    storage.delete(user)
    storage.save()

    return jsonify({}), 200


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Updates a User object by ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404, "User not found")

    user_data = request.get_json()
    if user_data is None:
        abort(400, "Not a JSON")

    ignore_keys = ["id", "email", "created_at", "updated_at"]
    for key, value in user_data.items():
        if key not in ignore_keys:
            setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict()), 200
