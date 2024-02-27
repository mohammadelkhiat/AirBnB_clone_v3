#!usr/bin/python3
""" places_amenities API """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from models import storage_t


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def places_amenities(place_id):
    """
        Endpoint to handle http methods for
        request to /places/<place_id>/amenities
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST', 'DELETE'])
def places_amenities_with_id(place_id, amenity_id):
    """
        Endpoint to handle http methods for
        request to /places/<place_id>/amenities/<amenity_id>
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if request.method == 'POST':
        if storage_t == 'db':
            if amenity in place.amenities:
                return jsonify(amenity.to_dict()), 200
            place.amenities.append(amenity)
        else:
            if amenity in place.amenities:
                return jsonify(amenity.to_dict()), 200
            place.amenity_ids.append(amenity_id)
        place.save()
        return jsonify(amenity.to_dict()), 201

    if request.method == 'DELETE':
        if storage_t == 'db':
            if amenity not in place.amenities:
                abort(404)
            place.amenities.remove(amenity)
        else:
            if amenity_id not in place.amenity_ids:
                abort(404)
            place.amenity_ids.remove(amenity_id)
        place.save()
        return jsonify({}), 200
