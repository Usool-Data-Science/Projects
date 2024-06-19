#!/usr/bin/python3
""" objects that handle all default RestFul API actions for suspects """
from flask import Flask, jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.complainant import Complainant
from models.suspect import Suspect


@app_views.route('/suspects', methods=['GET'], strict_slashes=False)
def get_suspects():
    """
    Retrieves the list of all Suspect objects
    """
    all_suspects = storage.all(Suspect).values()
    list_suspects = []
    for suspect in all_suspects:
        list_suspects.append(suspect.to_dict())
    return jsonify(list_suspects)


@app_views.route('/suspects/<suspect_id>', methods=['GET'], strict_slashes=False)
def get_spec_suspect(suspect_id):
    """ Retrieves a specific Suspect """
    suspect = storage.get(Suspect, suspect_id)
    if not suspect:
        abort(404)

    return jsonify(suspect.to_dict())


@app_views.route('/suspects/<suspect_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_suspect(suspect_id):
    """
    Deletes a Suspect Object
    """

    suspect = storage.get(Suspect, suspect_id)

    if not suspect:
        abort(404)

    storage.delete(suspect)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/suspects', methods=['POST'], strict_slashes=False)
def post_suspect():
    """
    Creates a Suspect
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Suspect(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/suspects/<suspect_id>', methods=['PUT'], strict_slashes=False)
def put_suspect(suspect_id):
    """
    Updates a Suspect
    """
    suspect = storage.get(Suspect, suspect_id)

    if not suspect:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(suspect, key, value)
    storage.save()
    return make_response(jsonify(suspect.to_dict()), 200)