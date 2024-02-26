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
            abort(404, 'Not a JSON')

        if 'name' not in data:
            abort(400, 'Missing name')

        new_amenity = Amenity(**data)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/api/v1/amenities/<amenity_id>', methods=['GET', ''])
def amenity_with_id(amenity_id):
    """Retrieves an amenity by id"""
    advantage = storage.get('Amenity', amenity_id)
    if advantage is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(advantage.to_dict())

    if request.method == 'DELETE':
        storage.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            abort(404, 'Not a JSON')

        for k, v in data.items():
            if k not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(advantage, k, v)
        advantage.save()
        return jsonify(advantage.to_dict()), 200
