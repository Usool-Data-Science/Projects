import os
import PyPDF2
from openai import OpenAI

from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

import quiz_it.processor
from quiz_it import app, bcrypt, db
from quiz_it.mcqs import mcqs
from quiz_it.prompt import get_mcq
from quiz_it.models import User, History, Question
from quiz_it.forms import RegistrationForm, LoginForm

@app.route("/", strict_slashes=False)
@app.route("/home", strict_slashes=False)
def home():
    """Renders the landing pages"""
    if current_user.is_authenticated:
        return redirect(url_for("upload"))
    return render_template("landing_page.html")

@app.route("/layout", strict_slashes=False)
def layout():
    return render_template('layout.html')

@app.route("/register", methods=['GET', 'POST'], strict_slashes=False)
def register():
    if current_user.is_authenticated:
        return redirect(url_for("upload"))
    form = RegistrationForm()
    if form.validate_on_submit():
        pasw_hs = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=pasw_hs,
            profession=form.profession.data,
            age=form.age.data,
            country=form.country.data,
            state=form.state.data,
            city=form.city.data,
            area_of_interest=form.area_of_interest.data,
            school=form.school.data,
            school_id=form.school_id.data
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Your account have been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'], strict_slashes=False)
def login():
    if current_user.is_authenticated:
        return redirect(url_for("upload"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("upload"))
        else:
            flash(f'Login not successful!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout", strict_slashes=False)
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/upload", methods=['GET', 'POST'], strict_slashes=False)
@login_required
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
