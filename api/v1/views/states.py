#!/usr/bin/python3
"""
A view for our state object
"""
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', strict_slashes=False)
def get_all_states():
    """get all the states"""
    all_state_objects = storage.all(State)

    states = [state.to_dict() for state in all_state_objects.values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state_by_id(state_id):
    """get a paticular state by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state_by_id(state_id):
    """deletes a particular state by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_a_state():
    """create a statw"""
    if not request.is_json or request.content_type != 'application/json':
        abort(400, description="Not a JSON")
    req_body = request.get_json()
    if 'name' not in req_body:
        abort(400, description="Missing name")
    new_state = State(**req_body)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update the status of a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.is_json or request.content_type != 'application/json':
        abort(400, description="Not a JSON")
    req_body = request.get_json()
    for key, val in req_body.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        setattr(state, key, val)
    state.save()
    return jsonify(state.to_dict()), 200
