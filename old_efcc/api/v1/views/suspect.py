#!/usr/bin/python3
""" objects that handle all default RestFul API actions for suspects """
import models
from flask import (Flask, flash, jsonify, make_response, abort,
                   request, redirect, url_for, render_template)
from api.v1.views import app_views
from api.v1.forms import SuspectForm
from api.v1.forms import IdentityForm
from api.v1.forms import FingerPrintForm
from models.base_model import BaseModel
from models.complainant import Complainant
from models.suspect import Suspect


# @app_views.route('/suspects', methods=['GET'], strict_slashes=False)
# def get_suspects():
#     """
#     Retrieves the list of all Suspect objects
#     """
#     all_suspects = models.storage.all(Suspect).values()
#     list_suspects = []
#     for suspect in all_suspects:
#         list_suspects.append(suspect.to_dict())
#     return jsonify(list_suspects)

summary = ['name', 'occupation', 'phone_no', 'nationality',
           'offence', 'gender', 'id']


@app_views.route('/suspects', methods=['GET'], strict_slashes=False)
def get_suspects():
    """
    Retrieves the list of all Suspect objects
    """
    suspectForm = SuspectForm()
    idForm = IdentityForm()
    fingerForm = FingerPrintForm()
    all_suspects = models.storage.all(Suspect).values()
    suspects = []
    for suspect in all_suspects:
        susp_dict = suspect.to_dict()
        susp = {k: susp_dict[k] for k in summary}
        suspects.append(susp)
    suspects.reverse()
    
    return render_template("suspect.html",
                           suspects=suspects[:5], title="Suspect",
                           sum_suspects=len(suspects),
                           suspectForm=suspectForm, idForm = idForm,
                           fingerForm = fingerForm)

@app_views.route('/suspects', methods=['POST'], strict_slashes=False)
def post_suspects():
    """
    Creates a Suspect
    """
    form = SuspectForm()
    if form.validate_on_submit():
        name = form.name.data
        instance = Suspect(name=form.name.data,
                           height=form.height.data,
                           skin_color=form.skin_color.data,
                           passport=form.passport.data,
                           mugshot=form.mugshot.data,
                           address=form.address.data,
                           nationality=form.nationality.data,
                           place_of_birth=form.place_of_birth.data,
                           gender=form.gender.data,
                           religion=form.religion.data,
                           occupation=form.occupation.data,
                           phone_no=form.phone_no.data,
                           parent_name=form.parent_name.data,
                           offence=form.offence.data)
        instance.save()
        flash(f'A new Suspect "{name}" has been created', 'success')
    else:
        flash('There is an error creating the Suspect', 'danger')
    return redirect(url_for('app_views.get_suspects'))

@app_views.route('/suspects/<suspect_id>', methods=['GET'], strict_slashes=False)
def get_spec_suspect(suspect_id):
    """ Retrieves a specific Suspect """
    suspect = models.storage.get(Suspect, suspect_id)
    if not suspect:
        abort(404)

    return jsonify(suspect.to_dict())


@app_views.route('/suspects/<suspect_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_suspect(suspect_id):
    """
    Deletes a Suspect Object
    """

    suspect = models.storage.get(Suspect, suspect_id)

    if not suspect:
        abort(404)

    models.storage.delete(suspect)
    models.storage.save()

    return make_response(jsonify({}), 200)


# @app_views.route('/suspects', methods=['POST'], strict_slashes=False)
# def post_suspect():
#     """
#     Creates a Suspect
#     """
#     if not request.get_json():
#         abort(400, description="Not a JSON")

#     if 'name' not in request.get_json():
#         abort(400, description="Missing name")

#     data = request.get_json()
#     instance = Suspect(**data)
#     instance.save()
#     return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/suspects/<suspect_id>', methods=['PUT'], strict_slashes=False)
def put_suspect(suspect_id):
    """
    Updates a Suspect
    """
    suspect = models.storage.get(Suspect, suspect_id)

    if not suspect:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(suspect, key, value)
    models.storage.save()
    return make_response(jsonify(suspect.to_dict()), 200)