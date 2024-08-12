#!/usr/bin/python3
"""
A view for the reviews for different
places
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.review import Review
from models.user import User
from models.place import Place
from models import storage


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_reviews_for_place(place_id):
    """
    Get all the reviews for a place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    all_reviews = storage.all(Review)
    reviews_for_place = [
            review.to_dict() for review in all_reviews.values() if
            review.place_id == place.id
            ]
    if len(reviews_for_place) < 0:
        abort(404)
    return jsonify(reviews_for_place)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review_by_id(review_id):
    """Get a review by the id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Delete a review by its id"""
    review_to_delete = storage.get(Review, review_id)
    if not review_to_delete:
        abort(404)
    else:
        storage.delete(review_to_delete)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_a_review(place_id):
    """Create a review for a specific place"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    req_body = request.get_json()
    if 'text' not in req_body:
        abort(400, "Missing text")
    if 'user_id' not in req_body:
        abort(400, "Missing user_id")
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    user = storage.get(User, req_body['user_id'])
    if not user:
        abort(404)
    extension = {"user_id": user.id, "place_id": place.id}
    req_body.update(extension)
    review = Review(**req_body)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_reviews(review_id):
    """Update the review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    req_body = request.get_json()
    for key, val in req_body.items():
        if key in ['id', 'user_id', 'place_id', 'create_at', 'updated_at']:
            continue
        setattr(review, key, val)
    review.save()
    return jsonify(review.to_dict()), 200
