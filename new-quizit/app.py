from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm
import os
import PyPDF2
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from mcqs import mcqs
import processor
from prompt import get_mcq


# we got the secret key using the secrets.token_hex(16) module
_ = load_dotenv(find_dotenv())

# Configure the application
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///quiz.db' 
app.config["SECRET_KEY"] = os.environ.get('APP_SECRET_KEY')
db = SQLAlchemy(app)
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

# Create the database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profession = db.Column(db.Enum('Student', 'Teacher', 'Others'), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(50))
    state = db.Column(db.String(50))
    city = db.Column(db.String(50))
    area_of_interest = db.Column(db.String(50))
    school = db.Column(db.String(50))
    school_id = db.Column(db.Integer, nullable=False)
    histories = db.relationship('History', backref='owner', lazy=True)
    questions = db.relationship('Question', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.id}')"

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.now)
    category = db.Column(db.String(20), nullable=False)
    export_type = db.Column(db.Enum('Download', 'On-page'))
    quiz_count = db.Column(db.Integer, nullable=False)
    user_mode = db.Column(db.Enum('Student', 'Teacher', 'Others'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mcqs = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"History('{self.id}', '{self.category}', '{self.quiz_count}')"


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.now)
    category = db.Column(db.String(20), nullable=False)
    quiz_count = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mcqs = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Question('{self.id}', '{self.category}', '{self.user_id}')"



@app.route("/", strict_slashes=False)
@app.route("/home", strict_slashes=False)
def home():
    """Renders the landing pages"""
    return render_template("landing_page.html")

@app.route("/layout", strict_slashes=False)
def layout():
    return render_template('layout.html')

@app.route("/register", methods=['GET', 'POST'], strict_slashes=False)
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'], strict_slashes=False)
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "ade@gmail.com" and form.password.data == "password":
            flash(f'Login successful!', 'success')
            return redirect(url_for('upload'))
        else:
            flash(f'Login not successful!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/upload", methods=['GET', 'POST'], strict_slashes=False)
def upload():
    if request.method == 'POST':
        if 'myFile' not in request.files:
            return "No file part"
        file = request.files['myFile']
        if file.filename == '':
            return "No selected file"
        if file and file.filename:
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            course_material = processor.read_file_content(file_path)
            question_count = 5
            # mcqs = get_mcq(material=course_material, question_count=question_count)
            return render_template("upload.html", title="Upload", mcqs=mcqs)
    return render_template("upload.html", title="Upload", mcqs=[])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)