#!/usr/bin/python3
""" users API """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'])
def users():
    """Retrieves the list of all user objects"""

    if request.method == 'GET':
        users = storage.all('User')
        users = [obj.to_dict() for obj in users.values()]
        return jsonify(users)

    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(404, 'Not a JSON')

        if 'email' not in data:
            abort(400, 'Missing email')

        if 'password' not in data:
            abort(400, 'Missing password')

        new_user = User(**data)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def user_with_id(user_id):
    """Retrieves a user by id"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())

    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            abort(404, 'Not a JSON')

        for k, v in data.items():
            if k not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, k, v)
        user.save()
        return jsonify(user.to_dict()), 200
