#!/usr/bin/python3
""" objects that handle all default RestFul API actions for petitions """
from flask import Flask, jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.complainant import Complainant
from models.petition import Petition


@app_views.route('/petitions', methods=['GET'], strict_slashes=False)
def get_petitions():
    """
    Retrieves the list of all Petition objects
    """
    all_petitions = storage.all(Petition).values()
    list_petitions = []
    for petition in all_petitions:
        list_petitions.append(petition.to_dict())
    return jsonify(list_petitions)


@app_views.route('/petitions/<petition_id>', methods=['GET'], strict_slashes=False)
def get_petition(petition_id):
    """ Retrieves a specific Petition """
    petition = storage.get(Petition, petition_id)
    if not petition:
        abort(404)

    return jsonify(petition.to_dict())


@app_views.route('/petitions/<petition_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_petition(petition_id):
    """
    Deletes a Petition Object
    """

    petition = storage.get(Petition, petition_id)

    if not petition:
        abort(404)

    storage.delete(petition)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/petitions', methods=['POST'], strict_slashes=False)
def post_petition():
    """
    Creates a Petition
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Petition(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/petitions/<petition_id>', methods=['PUT'], strict_slashes=False)
def put_petition(petition_id):
    """
    Updates a Petition
    """
    petition = storage.get(Petition, petition_id)

    if not petition:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(petition, key, value)
    storage.save()
    return make_response(jsonify(petition.to_dict()), 200)