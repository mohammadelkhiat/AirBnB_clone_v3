#!/usr/bin/python3
""" index view module """

from api.v1.views import app_views
from flask import jsonify
from models import storage as ST


@app_views.route('/status', methods=['GET'])
def status():
    """ Return status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """ Return the number of objects by type"""
    count = {}
    cls_to_table = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
        }
    {count.update({k: ST.count(v)}) for k, v in cls_to_table.items()}
    return jsonify(count)
