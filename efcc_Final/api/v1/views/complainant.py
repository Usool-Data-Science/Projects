#!/usr/bin/python3
""" objects that handle all default RestFul API actions for complainants """
from flask import (Flask, flash, jsonify, make_response, abort,
                   request, redirect, url_for, render_template)
from api.v1.views import app_views
from api.v1.forms import ComplainantForm
from models import storage
from models.base_model import BaseModel
from models.complainant import Complainant

@app_views.route('/complainants', methods=['GET'], strict_slashes=False)
def get_complainants():
    """
    Retrieves the list of all Complainant objects
    """
    form = ComplainantForm()
    all_complainants = storage.all(Complainant).values()
    complainants = []
    for complainant in all_complainants:
        compln = complainant.to_dict()
        if "__class__" in compln:
            del compln["__class__"]
        complainants.append(compln)
    complainants.reverse()
    return render_template("complainant.html",
                        complainants = complainants[:5], title="Complainant",
                        sum_complainants = len(complainants), form=form)

@app_views.route('/complainants', methods=['POST'], strict_slashes=False)
def post_complainants():
    """
    Creates a Complainant
    """
    # if not request.get_json():
    #     abort(400, description="Not a JSON")

    # if 'name' not in request.get_json():
    #     abort(400, description="Missing name")
    # data = request.get_json()
    # instance = Complainant(**data)
    # return make_response(jsonify(instance.to_dict()), 201)

    form = ComplainantForm()
    if form.validate_on_submit():
        print("FORM IS AVAILABLE")
        name = form.name.data
        instance = Complainant(name=form.name.data,
                    address=form.address.data,
                    nationality=form.nationality.data,
                    state=form.state.data,
                    gender=form.gender.data, 
                    age=form.age.data,
                    occupation=form.occupation.data, 
                    religion=form.religion.data,
                    education=form.education.data,
                    phone_no=form.phone.data)
        instance.save()
        flash(f'A new Complainant {[name]} has been created', 'success')
    else:
        flash(f'There is an error creating Complainant {[name]}', 'danger')
    return redirect(url_for('app_views.get_complainants'))

# @app_views.route('/complainants', methods=['GET', 'POST'], strict_slashes=False)
# def manage_complainants():
#     """
#     Retrieves the list of all Complainant objects
#     """
#     all_complainants = storage.all(Complainant).values()
#     complainants = []
#     for complainant in all_complainants:
#         compln = complainant.to_dict()
#         if "__class__" in compln:
#             del compln["__class__"]
#         complainants.append(compln)
#     form = ComplainantForm()
#     if request.method == 'POST':
#         if form.validate_on_submit():
#             print("FORM IS AVAILABLE")
#             name = form.name.data
#             instance = Complainant(name=form.name.data,
#                         address=form.address.data,
#                         nationality=form.nationality.data,
#                         state=form.state.data,
#                         gender=form.gender.data, 
#                         age=form.age.data,
#                         occupation=form.occupation.data, 
#                         religion=form.religion.data,
#                         education=form.education.data,
#                         phone_no=form.phone.data)
#             instance.save()
#             flash(f'A new Complainant {[name]} has been created', 'success')
#         else:
#             flash(f'There is an error creating Complainant {[name]}', 'danger')        
#     return render_template("complainant.html",
#                         complainants = complainants[-5:], title="Complainant",
#                         sum_complainants = len(complainants), form=form)

@app_views.route('/complainants/<complainant_id>', methods=['GET'], strict_slashes=False)
def get_Complainant(complainant_id):
    """ Retrieves a specific Complainant """
    complainant = storage.get(Complainant, complainant_id)
    if not complainant:
        abort(404)

    return jsonify(complainant.to_dict())


@app_views.route('/complainants/<complainant_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_Complainant(complainant_id):
    """
    Deletes a Complainant Object
    """

    complainant = storage.get(Complainant, complainant_id)

    if not complainant:
        abort(404)

    storage.delete(complainant)
    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('/complainants/<complainant_id>', methods=['PUT'], strict_slashes=False)
def put_Complainant(complainant_id):
    """
    Updates a Complainant
    """
    complainant = storage.get(Complainant, complainant_id)

    if not complainant:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(Complainant, key, value)
    storage.save()
    return make_response(jsonify(complainant.to_dict()), 200)