#!/usr/bin/python3
""" API module """

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv


app = Flask(__name__)
app.url_map.strict_slashes = False

host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', '5000')

app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """ 404 error handler """
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_appcontext(response_or_exc):
    """ close the session """
    storage.close()


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True),
