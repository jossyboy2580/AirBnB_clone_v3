#!/usr/bin/python3
"""
A view for our amenity object
"""
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', strict_slashes=False)
def get_all_amenities():
    """get all the amenities"""
    all_amenities = storage.all(Amenity)

    amenities = [amenity.to_dict() for amenity in all_amenities.values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """get a paticular amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    else:
        return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity_by_id(amenity_id):
    """deletes a particular amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_an_amenity():
    """create an amenity"""
    req_body = request.get_json()
    if request.content_type != 'application/json' or not request.is_json:
        abort(400, description="Not a JSON")
    if 'name' not in req_body:
        abort(400, description="Missing name")
    new_amenity = Amenity(**req_body)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """update the status of an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    req_body = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    for key, val in req_body.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        setattr(amenity, key, val)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
