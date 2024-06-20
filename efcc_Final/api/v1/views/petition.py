#!/usr/bin/python3
""" objects that handle all default RestFul API actions for petitions """
from flask import (Flask, flash, jsonify, make_response, abort,
                   request, redirect, url_for, render_template)
from api.v1.views import app_views
from api.v1.forms import ComplainantForm
from models import storage
from models.base_model import BaseModel
from models.complainant import Complainant
from models.petition import Petition
from api.v1.forms import PetitionForm

@app_views.route('/petitions', methods=['GET'], strict_slashes=False)
def get_petitions():
    """
    Retrieves the list of all Petition objects
    """
    form = PetitionForm()
    all_petitions = storage.all(Petition).values()
    petitions = []
    for petition in all_petitions:
        petn = petition.to_dict()
        if "__class__" in petn:
            del petn["__class__"]
        petitions.append(petn)
    petitions.reverse()
    return render_template("petition.html",
                        petitions=petitions[:5], title="Petition",
                        sum_petitions=len(petitions), form=form)

@app_views.route('/petitions', methods=['POST'], strict_slashes=False)
def post_petitions():
    """
    Creates a Petition
    """
    form = PetitionForm()
    if form.validate_on_submit():
        print("FORM IS AVAILABLE")
        title = form.title.data
        instance = Petition(title=form.title.data,
                    description=form.description.data,
                    complainant_id=form.complainant_id.data,
                    status=form.status.data)
        instance.save()
        flash(f'A new Petition titled "{title}" has been created', 'success')
    else:
        flash('There is an error creating the Petition', 'danger')
    return redirect(url_for('app_views.get_petitions'))



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