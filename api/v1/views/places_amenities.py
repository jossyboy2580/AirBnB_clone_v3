#!/usr/bin/python3
"""
A module with a flask blueprint view for amenities
in a place
"""
from flask import request, jsonify, abort
from models.place import Place
from models.amenity import Amenity
from models import storage
import models
from api.v1.views import api_views


@api_views.route('/places/<place_id>/amenities', strict_slashes=False)
def get_amenities_in_a_place(place_id):
    """ Get all the amenities in a paticular place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenities =  storage.all(Amenity)
    amenities_in_place = [amenity.to_dict()
                          for amenity in amenities.values()
                          if amenity.id == place_id]
    return jsonify(amenities_in_place), 200


@api_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_an_amenity_from_a_place(place_id, amenity_id):
    """ Delete an amenity from a place by the id of the amenity
        and that of the place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not amenity_id in place.amenity_ids:
        abort(404)
    if models.storage_t == 'db':
        session = models.storage._DBStorage__session
        # do the rest work regarding db storage
    else:
        # other work for the file storage
