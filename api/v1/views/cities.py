#!/usr/bin/python3
""" cities API """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities(state_id):
    """ Endpoint to handle http methods for request to /cities"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        return jsonify([city.to_dict() for city in state.cities])

    if request.method == 'POST':
        data = request.get_json()
        print(data)
        if data is None:
            return jsonify({"error": "Not a JSON"}), 400
        if 'name' not in data:
            return jsonify({"error": "Missing name"}), 400
        data['state_id'] = state_id
        new_city = City(**data)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def city_with_id(city_id):
    """ Retrieves a City object by id"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Not a JSON"}), 400
        for k, v in data.items():
            if k not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, k, v)
        city.save()
        return jsonify(city.to_dict()), 200
