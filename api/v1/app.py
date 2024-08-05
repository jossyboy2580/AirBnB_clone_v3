#!/usr/bin/python3
"""
The entry point of our flask app
"""
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)

app.register_blueprint(app_views, url_prefix='/api/v1/')


@app.teardown_appcontext
def close_storage(exception):
    """This method closes the storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(400)
def handle_400_error(error):
    response = jsonify({"error": error.description})
    response.status_code = 400
    return response


if __name__ == '__main__':
    HOST = os.getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(os.getenv('HBNB_API_PORT', 5000))

    app.run(host=HOST, port=PORT, threaded=True)
