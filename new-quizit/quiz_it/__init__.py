import os
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask_login import LoginManager

# we got the secret key using the secrets.token_hex(16) module
_ = load_dotenv(find_dotenv())

# Configure the application
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///quiz.db' 
app.config["SECRET_KEY"] = os.environ.get('APP_SECRET_KEY')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

"""
This is needed to create the instance of our db within app context, when you
include app.app_context().push() in the config and then import the db from app,
you will see an instance folder being created and then when you run .create_all()
you will see your acqual .db file created. And use db.drop_all() to erase  all commits.
If you dont want it to be stored in instance folder by default, do these.

basedir = os.path.abspath(os.path.dirname(file))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
"""
app.app_context().push()

from quiz_it import routes