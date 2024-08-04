#!/usr/bin/python3
"""
an init file for our views
"""
from flask import Blueprint
from api.v1.views.index import *


app_views = Blueprint('app_views', __name__)


@app_views.route('/status')
def api_status():
    """return the status of the api"""
    return jsonify({"status": "OK"})
