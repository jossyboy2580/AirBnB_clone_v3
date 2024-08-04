#!/usr/bin/python3
"""
all the index for our app
"""
from flask import jsonify
from models import storage
from api.v1.views import app_views
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.state import State
from models.city import City
from models.review import Review


@app_views.route('/status')
def api_status():
    """return the status of the api"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def object_count():
    """retrieve the number of each object by type"""
    counts = {'amenities': storage.count(Amenity),
              'cities': storage.count(City),
              'places': storage.count(Place),
              'reviews': storage.count(Review),
              'states': storage.count(State),
              'users': storage.count(User)}
    return jsonify(counts)
