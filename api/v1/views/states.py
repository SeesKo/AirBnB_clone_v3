#!/usr/bin/python3
"""
API endpoints for managing 'State' objects in a RESTful manner.
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Returns a list of all State objects"""
    all_states = storage.all(State).values()
    states_list = [state.to_dict() for state in all_states]
    return jsonify(states_list)


@app_views.route("/states/<state_id>", strict_slashes=False)
def get_state(state_id):
    """Returns a State object by ID"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        return abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object by ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Creates a new State"""
    if request.content_type != "application/json":
        return abort(404, "Not a JSON")
    if not request.get_json():
        return abort(400, "Not a JSON")

    kwargs = request.get_json()

    if "name" not in kwargs:
        abort(400, "Missing name")

    new_state = State(**kwargs)
    new_state.save()
    return jsonify(new_state.to_dict()), 200


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Updates a State object by ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    state_data = request.json
    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in state_data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict())