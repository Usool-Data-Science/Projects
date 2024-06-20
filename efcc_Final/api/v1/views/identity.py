""" objects that handle all default RestFul API actions for petitions """
from flask import (Flask, flash, jsonify, make_response, abort,
                   request, redirect, url_for, render_template)
from api.v1.views import app_views
from models.identity import Identity
from api.v1.forms import IdentityForm


@app_views.route('/identities', methods=['GET'], strict_slashes=False)
def get_identities():
    """
    Retrieves the list of all Identity objects
    """
    form = IdentityForm()
    all_identities = storage.all(Identity).values()
    identities = []
    for identity in all_identities:
        idn = identity.to_dict()
        if "__class__" in idn:
            del idn["__class__"]
        identities.append(idn)
    identities.reverse()
    return render_template("identity.html",
                           identities=identities[:5], title="Identity",
                           sum_identities=len(identities), form=form)

@app_views.route('/identities', methods=['POST'], strict_slashes=False)
def post_identities():
    """
    Creates an Identity
    """
    form = IdentityForm()
    if form.validate_on_submit():
        print("FORM IS AVAILABLE")
        id_type = form.id_types.data
        instance = Identity(id_types=form.id_types.data,
                            id_number=form.id_number.data,
                            suspect_id=form.suspect_id.data)
        instance.save()
        flash(f'A new Identity has been created', 'success')
    else:
        flash('There is an error creating the Identity', 'danger')
    return redirect(url_for('app_views.get_identities'))
