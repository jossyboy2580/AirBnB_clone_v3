#!/usr/bin/python3
"""
The entry point of our flask app
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
CORS(app, resorces=r"/*", origins=r"0.0.0.0")

app.register_blueprint(app_views, url_prefix='/api/v1/')


@app.teardown_appcontext
def close_storage(exception):
    """This method closes the storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """page not found"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(400)
def handle_400_error(error):
    """handle all the 400 errors"""
    return jsonify({"error": error.description}), 400


if __name__ == '__main__':
    HOST = os.getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(os.getenv('HBNB_API_PORT', 5000))

    app.run(host=HOST, port=PORT, threaded=True)
