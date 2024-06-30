#!/usr/bin/python3
"""A flask application that runs the endpoints"""
from flask import Flask, render_template, make_response, jsonify
from os import getenv
from dotenv import load_dotenv

# Extension importation
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# Custom modules
from api.v1.views import app_views
import models

staffs = models.newStaff

# Import Environment Variables
load_dotenv()

# App Creation
app = Flask(__name__)
app.register_blueprint(app_views)
app.config["SECRET_KEY"] = getenv('APP_SECRET_KEY')
app.app_context().push()

# Extension Instantiation
bcrypt = Bcrypt()
login_manager = LoginManager()
admin = Admin()

# Extension Initializaiton
admin.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'app_views.login'
login_manager.login_message_category = 'info'

# Add a new view to the admin page
admin.add_view(ModelView(Staff, models.storage))

@login_manager.user_loader
def load_user(user_id):
    """
        Retrieves user with a particular ID, It however expect our user model
        to have the following 4 attributes at least:
        1. is_authenticated: returns true if the user provided valid credentials
        2. is_active 3. is_anonymous 4.get_id()
            All these are available in flask_login and its called UserMixin.
            So ensure the Staff model is inheriting from UserMixin to get these
            four attributes
    """
    import models
    from models.staff import Staff
    staff = models.storage.get(Staff, int(user_id))
    if staff:
        return staff
    else:
        return None

@app.teardown_appcontext
def close_db(error):
    """Closes the data"""
    from console import storage
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Custom error message"""
    response = jsonify({'error': 'Not Found'})
    return make_response(response)


if __name__ == "__main__":
    """Module runner"""
    # host = getenv("EFCC_MYSQL_HOST")
    # port = getenv("EFCC_MYSQL_PORT")
    # if not host:
    #     host = '0.0.0.0'
    # if not port:
    #     port = '5000'
    # app.run(host=host, port=port, threaded=True, debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
