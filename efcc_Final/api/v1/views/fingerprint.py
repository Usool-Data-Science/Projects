""" objects that handle all default RestFul API actions for petitions """
from flask import (Flask, flash, jsonify, make_response, abort,
                   request, redirect, url_for, render_template)
from api.v1.views import app_views
from api.v1.forms import ComplainantForm
from models.fingerprint import FingerPrint
from api.v1.forms import FingerPrintForm

@app_views.route('/fingerprints', methods=['GET'], strict_slashes=False)
def get_fingerprints():
    """
    Retrieves the list of all FingerPrint objects
    """
    form = FingerPrintForm()
    all_fingerprints = storage.all(FingerPrint).values()
    fingerprints = []
    for fingerprint in all_fingerprints:
        fp = fingerprint.to_dict()
        if "__class__" in fp:
            del fp["__class__"]
        fingerprints.append(fp)
    fingerprints.reverse()
    return render_template("fingerprint.html",
                           fingerprints=fingerprints[:5], title="Fingerprint",
                           sum_fingerprints=len(fingerprints), form=form)

@app_views.route('/fingerprints', methods=['POST'], strict_slashes=False)
def post_fingerprints():
    """
    Creates a FingerPrint
    """
    form = FingerPrintForm()
    if form.validate_on_submit():
        print("FORM IS AVAILABLE")
        finger_print = form.finger_print.data
        instance = FingerPrint(finger_print=form.finger_print.data,
                               mugshot=form.mugshot.data,
                               suspect_id=form.suspect_id.data)
        instance.save()
        flash(f'A new FingerPrint has been created', 'success')
    else:
        flash('There is an error creating the FingerPrint', 'danger')
    return redirect(url_for('app_views.get_fingerprints'))
