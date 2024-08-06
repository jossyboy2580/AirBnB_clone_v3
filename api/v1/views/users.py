#!/usr/bin/python3
"""
A view for our user object
"""
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', strict_slashes=False)
def get_all_users():
    """get all the users"""
    all_users = storage.all(User)

    users = [user.to_dict() for user in all_users.values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user_by_id(user_id):
    """get a paticular user by id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    """deletes a particular user by id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_a_user():
    """create a user"""
    req_body = request.get_json()
    if request.content_type != 'application/json' or not request.is_json:
        abort(400, description="Not a JSON")
    if 'email' not in req_body:
        abort(400, description="Missing name")
    if 'password' not in req_body:
        abort(400, description="Missing password")
    new_user = User(**req_body)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """update the status of a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    req_body = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    for key, val in req_body.items():
        if key in ['id', 'email', 'created_at', 'updated_at']:
            continue
        setattr(user, key, val)
    user.save()
    return jsonify(user.to_dict()), 200
