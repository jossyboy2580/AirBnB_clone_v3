#!/usr/bin/python3
"""
The entry point of our flask app
"""
import os
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)

app.register_blueprint(app_views, url_prefix='/api/v1/')


@app.teardown_appcontext
def close_storage(exception):
    """This method closes the storage"""
    storage.close()


if __name__ == '__main__':
    HOST = os.getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(os.getenv('HBNB_API_PORT', 5000))

    app.run(host=HOST, port=PORT, threaded=True)
