#!/usr/bin/python3
""" amenities API """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'])
def amenities():
    """Retrieves the list of all amenity objects"""

    if request.method == 'GET':
        amenities = storage.all('Amenity')
        amenities = [obj.to_dict() for obj in amenities.values()]
        return jsonify(amenities)

    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Not a JSON"}), 400

        if 'name' not in data:
            return jsonify({"error": "Missing name"}), 400

        new_amenity = Amenity(**data)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenity_with_id(amenity_id):
    """Retrieves an amenity by id"""
    advantage = storage.get('Amenity', amenity_id)
    if advantage is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(advantage.to_dict())

    if request.method == 'DELETE':
        storage.delete(advantage)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Not a JSON"}), 400

        for k, v in data.items():
            if k not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(advantage, k, v)
        advantage.save()
        return jsonify(advantage.to_dict()), 200
