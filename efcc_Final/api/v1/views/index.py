from flask import Flask, jsonify, render_template
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.complainant import Complainant
from models.suspect import Suspect
from models.fingerprint import FingerPrint
from models.identity import Identity
from models.petition import Petition
from models.recovery import (Monetary, Bank, Crypto, Cash, Recovery,
                                Electronic, Phone, Laptop, Other,
                                Automobile, Jewelry, LandedProperty)

@app_views.route("/status", strict_slashes=False)
def status():
    return jsonify({"status": "OK!"})

@app_views.route("/", strict_slashes=False)
@app_views.route("/dashboard", strict_slashes=False)
def home():
    response = []
    all_petitions = list(storage.all(Petition).values())
    """Get complainants names"""
    for petition in all_petitions:
        petition_dict = {}

        petition_dict['Case File #'] = petition.casefile_no
        petition_dict['Credential #'] = petition.cr_no
        petition_dict['Date Assigned'] = petition.date_assigned

        complainant_names = [str(compt.name) for compt in petition.complainants]
        petition_dict['Complainants'] = ", ".join(complainant_names)

        petition_dict['Amount'] = petition.amount_involved
        petition_dict['Source'] = petition.petition_source 
        petition_dict['Status'] = petition.status_signal
        
        response.append(petition_dict)   

    return render_template("dashboard.html",
                           dashboard_result_list = response,
                           sum_petition=len(all_petitions))

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Retrieves the number of each objects by type """

    classes = {"Complainant": Complainant, "Suspect": Suspect,
            "FingerPrint": FingerPrint, "Identity": Identity, "Petition": Petition,
            "Monetary": Monetary, "Bank": Bank, "Crypto": Crypto, "Cash": Cash,
            "Recovery": Recovery, "Electronic": Electronic, "Phone": Phone,
            "Laptop": Laptop, "Other": Other, "Automobile": Automobile,
            "Jewelry": Jewelry, "LandedProperty": LandedProperty}

    num_objs = {}
    for k,v in classes.items():
        if k != "BaseModel":
            num_objs[k] = storage.count(v)

    return jsonify(num_objs)