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
    host = os.getenv('')
    if not host:
        host = '0.0.0.0'
    port = os.getenv('')
    if not port:
        port = 5000
    else:
        port = int(port)

    app.run(host=host, port=port, threaded=True)
