#!/usr/bin/python3
"""
A view for our state object
"""
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_all_places_with_city(city_id):
    """get all places for the city"""
    all_places = storage.all(Place)
    linked_city = storage.get(City, city_id)
    if not linked_city:
        abort(404)

    places = [place.to_dict() for place in all_places.values()
            if place.city_id == city_id]
    if len(places) < 0:
        abort(404)
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place_by_id(place_id):
    """get a paticular place by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place_by_id(place_id):
    """deletes a particular place by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
        strict_slashes=False)
def create_a_place(city_id):
    """create a plsce"""
    if request.content_type != 'application/json' or not request.is_json:
        abort(400, description="Not a JSON")
    req_body = request.get_json()
    if 'name' not in req_body:
        abort(400, description="Missing name")
    if 'user_id' not in req_body:
        abort(400, description="Missing user_id")
    linked_city = storage.get(City, city_id)
    if not linked_city:
        abort(404)
    linked_user = storage.get(User, req_body['user_id'])
    if not linked_user:
        abort(404)
    dict_extension = {'city_id': city_id, 'user_id': req_body['user_id']}
    req_body.update(dict_extension)
    new_place = Place(**req_body)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """update the status of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    req_body = request.get_json()
    for key, val in req_body.items():
        if key in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            continue
        setattr(place, key, val)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_place():
    """Endpoint to return all the places"""
    if not request.is_json:
        abort(400, description='Not a JSON')
    req_body = request.get_json()
    all_places = storage.all(Place)
    all_cities = storage.all(City)
    cities_in_request = []
    result = all_places

    # Get the value for each of the possible keys
    # if it returns None then pass
    state_ids = req_body.get('states')
    if state_ids:
        for city in all_cities:
            if city.state_id in state_ids:
                cities_in_request.append(city)
    city_ids = req_body.get('cities')
    if city_ids:
        for city in all_cities:
            if city.id in city_ids:
                cities_in_request.append(city)
    seen = set()
    unique_cities_in_request = []
    for city in cities_in_request:
        if city.id in seen:
            continue
        seen.add(city.id)
        unique_cities_in_request.append(city)
    amenity_ids = req_body.get('amenities')
    if amenity_ids:
        result = []
        if len(cities_in_request) >= 1:
            cities_in_request_ids = [city.id
                                     for city in unique_cities_in_request]
            all_places = [place for place in all_places
                          if place.city_id in cities_in_request_ids]
            for place in all_places:
                if sorted(place.amenity_ids) == sorted(amenity_ids):
                    result.append(place)
    result = [all_places[place].to_dict() for place in result]
    return jsonify(result), 200
