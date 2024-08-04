#!/usr/bin/python3
"""
A view for our state object
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities/', methods=['GET'])
def get_all_cities_for_states(state_id):
    """get all cities for the state"""
    all_city_objects = storage.all(City)

    cities = [city for city in all_city_objects.values()]
    cities_for_state = list(filter(lambda city: city.id == state_id, cities))
    if len(cities_for_state) < 1:
        abort(404)
    state_cities = [city.to_dict() for city in cities_for_state]
    return jsonify(state_cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
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


@app_views.route('states/<state_id>/cities/', methods=['POST'])
def create_a_city(state_id):
    """create a city"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    req_body = request.get_json()
    if not isinstance(req_body, dict):
        response = jsonify({"error": "Not a JSON"})
        response.status_code = 400
        return response
    if 'name' not in req_body:
        response = jsonify({"error": "Missing name"})
        response.status_code = 400
        return response
    new_city = City(**req_body)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('cities/city_id>', methods=['PUT'])
def update_city(city_id):
    """update the status of a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    req_body = request.get_json()
    if not isinstance(req_body, dict):
        response = jsonify({"error": "Not a JSON"})
        response.status_code = 400
        return response
    for key, val in req_body.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict()), 200
