from flask_wtf import FlaskForm
from quiz_it.models import User
from wtforms import (StringField, PasswordField, SubmitField,
                     IntegerField, SelectField, BooleanField)
from wtforms.validators import (DataRequired, Email, EqualTo, 
                                Length, NumberRange, ValidationError)


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=60)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    profession = SelectField('Profession', choices=[('Student', 'Student'), ('Teacher', 'Teacher'), ('Others', 'Others')], validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=1, message='Age must be positive')])
    country = StringField('Country', validators=[Length(max=50)])
    state = StringField('State', validators=[Length(max=50)])
    city = StringField('City', validators=[Length(max=50)])
    area_of_interest = StringField('Area of Interest', validators=[Length(max=50)])
    school = StringField('School', validators=[Length(max=50)])
    school_id = IntegerField('School ID', validators=[DataRequired(), NumberRange(min=1, message='School ID must be positive')])
    submit = SubmitField('Sign Up')
    reset = SubmitField('Clear All', render_kw={"type": "reset"})

    def validate_email(self, email):
        """Check if the email is already taken"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose another email!")
    
    def validate_password(self, password):
        """Check if password is less than 6 digits"""
        pasw = len(password.data)
        if pasw < 6:
            raise ValidationError("Password can not be less than 6 characters!")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')