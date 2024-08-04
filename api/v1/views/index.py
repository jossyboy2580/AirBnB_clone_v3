#!/usr/bin/python3
"""
all the index for our app
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def api_status():
    """return the status of the api"""
    return jsonify({"status": "OK"})
