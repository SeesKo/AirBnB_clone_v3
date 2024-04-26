#!/usr/bin/python3
"""
API endpoints for managing 'State' objects in a RESTful manner.
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"])
def get_states():
    """Returns a list of all State objects"""
    states = []
    for v in storage.all("State").values():
        states.append(v.to_dict())
    return (jsonify(states))


@app_views.route("/states/<state_id>", methods=["GET"])
def get_state(state_id):
    """Returns a State object by ID"""
    if state_id is None:
        states = storage.all("State")
        get_state = [value.to_dict() for key, value in states.items()]
        return (jsonify(get_state))
    get_state = storage.get("State", state_id)
    if get_state is not None:
        return (jsonify(get_state.to_dict()))
    abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Deletes a State object by ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route("/states", methods=["POST"])
def create_state():
    """Creates a new State"""
    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.json:
        abort(400, "Missing name")
    state_data = request.json
    new_state = State(name=state_data["name"])
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
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
