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

    places = [place.to_dict() for place in all_places.values()
              if place.city_id == city_id]
    if len(places) < 1:
        abort(404)
    city_places = [place.to_dict() for place in places]
    return jsonify(city_places)


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


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_a_place(city_id):
    """create a plsce"""
    req_body = request.get_json()
    if request.content_type != 'application/json' or not request.is_json:
        abort(400, description="Not a JSON")
    if 'email' not in req_body:
        abort(400, description="Missing name")
    if 'user_id' not in req_body:
        abort(400, description="Missing user_id")
    linked_city = storage.get(City, city_id)
    if not linked_city:
        abort(404)
    linked_user = storage.get(User, req_body['user_id'])
    if not linked_user:
        abort(404)
    dict_extension = {'city_id': city_id, 'user_id':req_body['user_id']}
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
    req_body = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    for key, val in req_body.items():
        if key in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            continue
        setattr(place, key, val)
    place.save()
    return jsonify(place.to_dict()), 200
