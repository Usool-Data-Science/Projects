from flask import Flask, render_template, url_for
from models import storage

app = Flask(__name__)

@app.route('/dashboard', strict_slashes=False)
def dashboard():
    return render_template("dashboard.html")

@app.route('/petitions', strict_slashes=False)
def petition():
    all_petition = storage.all("Petition").values()
    return render_template("petition.html", petitions=all_petition)

@app.route('/complainants', strict_slashes=False)
def complainant():
    all_complainant = storage.all("Complainant").values()
    return render_template("complainant.html", complainants=all_complainant)

@app.route('/suspects', strict_slashes=False)
def suspect():
    all_suspect = storage.all("Suspect").values()
    return render_template("suspect.html", suspects=all_suspect)

@app.route('/recoveries', strict_slashes=False)
def recoveries():
    all_recoveries = storage.all("Recovery").values()
    return render_template("recovery.html", recoveries=all_recoveries)

@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)