#!/usr/bin/python3
"""
A view for our city object
"""
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_all_cities_for_states(state_id):
    """get all cities for the state"""
    all_city_objects = storage.all(City)
    linked_state = storage.get(State, state_id)
    if not linked_state:
        abort(404)

    cities = [city for city in all_city_objects.values()
              if city.state_id == state_id]
    if len(cities) < 0:
        abort(404)
    state_cities = [city.to_dict() for city in cities]
    return jsonify(state_cities)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city_by_id(city_id):
    """get a paticular city by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city_by_id(city_id):
    """deletes a particular city by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_a_city(state_id):
    """create a city"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    c_type = request.content_type
    if not request.is_json or c_type != 'application/json':
        abort(400, description="Not a JSON")
    req_body = request.get_json()
    if 'name' not in req_body:
        response = make_response(jsonify({"error": "Missing name"}), 400)
        abort(400, description="Missing name")
    linked_state = storage.get(State, state_id)
    if not linked_state:
        abort(404)
    linked_state_dict = {'state_id': state_id}
    req_body.update(linked_state_dict)
    new_city = City(**req_body)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """update the status of a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json or request.content_type != 'application/json':
        abort(400, description="Not a JSON")
    req_body = request.get_json()
    for key, val in req_body.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict()), 200
