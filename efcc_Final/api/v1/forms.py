import email_validator
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField,
                     IntegerField, SelectField, BooleanField,
                     TelField, DateTimeField)
from wtforms.validators import (DataRequired, Email, EqualTo,
                                Length, NumberRange, ValidationError,
                                URL)

from models.staff import Staff
from models import storage

id_cards = ('Licence', 'NIN', 'Passport')
nigeria_skin_colors = ['Dark Brown', 'Brown', 'Light Brown', 'Dark', 'Fair', 'Caramel']
religion_types = ['Islam', 'Christianity', 'Traditional', 'Others']
offence_types = ["False Pretence", "Impersonation", "Forgery", "Conspiracy",
                 "Aiding and Abetting", "Stealing", "Theft", "Bribery", "Tax Evasion"]
nigeria_states = ("Abia", "Abuja", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi",
                  "Bayelsa", "Benue", "Borno", "Cross River", "Delta",
                  "Ebonyi", "Edo", "Ekiti", "Enugu", "Gombe", "Imo",
                  "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi",
                  "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger",
                  "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers",
                  "Sokoto", "Taraba", "Yobe", "Zamfara")

class ComplainantForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=30)])
    address = StringField('Address', validators=[DataRequired(), Length(max=50)])
    nationality = StringField('Nationality', validators=[DataRequired(), Length(max=50)])
    # state = StringField('State', validators=[DataRequired(), Length(max=50)])
    state = SelectField('State', choices=[(val, val) for val in nigeria_states], validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'),('Female', 'Female')])
    age = IntegerField('Age', validators=[DataRequired(), DataRequired(), NumberRange(min=1, message='Age must be positive')])
    occupation = StringField('Occupation', validators=[DataRequired(), Length(max=50)])
    religion = SelectField('Religion', choices=[('Islam', 'Islam'),('Christianity', 'Christianity'),('Traditional', 'Traditional'), ('Others', 'Others')])
    education = SelectField('Education', choices=[('Primary','Primary'), ('Secondary', 'Secondary'), ('Tertiary', 'Tertiary')])
    phone = TelField('Phone Number', validators=[DataRequired()])
    
    submit = SubmitField('Submit')
    reset = SubmitField('Reset', render_kw={"type": "reset"})

class PetitionForm(FlaskForm):
    casefile_no = StringField('Case File No', validators=[DataRequired(), Length(max=50)])
    cr_no = StringField('CR No', validators=[DataRequired(), Length(max=50)])
    date_received = DateTimeField('Date Received', format='%Y-%m-%d %H:%M:%S', default=datetime.now(), validators=[DataRequired()])
    date_assigned = DateTimeField('Date Assigned', format='%Y-%m-%d %H:%M:%S', default=datetime.now(), validators=[DataRequired()])
    amount_involved = IntegerField('Amount Involved', validators=[NumberRange(min=0, message='Amount must be positive')])
    status_signal = SelectField('Status Signal', choices=[('Convicted', 'Convicted'), ('In-Progress', 'In-Progress')])
    petition_source = SelectField('Petition Source', choices=[('Intelligence', 'Intelligence'), ('Regular-Complain', 'Regular-Complain')])
    
    submit = SubmitField('Submit')
    reset = SubmitField('Reset', render_kw={"type": "reset"})

class SuspectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=128)])
    height = IntegerField('Height (cm)', validators=[DataRequired(), NumberRange(min=1, message='Height must be positive')])
    skin_color = SelectField('Skin Color', choices=[(val, val) for val in nigeria_skin_colors], validators=[DataRequired()])
    passport = StringField('Passport URL', validators=[DataRequired(), Length(max=255)])
    mugshot = StringField('Mugshot URL', validators=[DataRequired(), Length(max=255)])
    address = StringField('Address', validators=[DataRequired(), Length(max=50)])
    nationality = StringField('Nationality', validators=[DataRequired(), Length(max=20)], default="Nigerian")
    place_of_birth = StringField('Place of Birth', validators=[DataRequired(), Length(max=50)])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    religion = SelectField('Religion', choices=[(val, val) for val in religion_types], validators=[DataRequired()])
    occupation = StringField('Occupation', validators=[DataRequired(), Length(max=50)])
    phone_no = StringField('Phone Number', validators=[DataRequired(), Length(max=15)])
    parent_name = StringField('Parent Name', validators=[DataRequired(), Length(max=50)])
    offence = SelectField('Offence', choices=[(val, val) for val in offence_types], validators=[DataRequired()])

    submit = SubmitField('Submit')
    reset = SubmitField('Reset', render_kw={"type": "reset"})

class FingerPrintForm(FlaskForm):
    finger_print = StringField('Fingerprint', validators=[DataRequired(), Length(max=128)])
    mugshot = StringField('Mugshot URL', validators=[DataRequired(), Length(max=128), URL()])
    suspect_id = IntegerField('Suspect ID', validators=[DataRequired(), NumberRange(min=1, message='Suspect ID must be positive')])

    submit = SubmitField('Submit')
    reset = SubmitField('Reset', render_kw={"type": "reset"})

class IdentityForm(FlaskForm):
    id_types = SelectField('ID Type', choices=[(val, val) for val in id_cards], validators=[DataRequired()])
    id_number = IntegerField('ID Number', validators=[DataRequired(), NumberRange(min=1, message='ID Number must be positive')])
    suspect_id = IntegerField('Suspect ID', validators=[DataRequired(), NumberRange(min=1, message='Suspect ID must be positive')])

    submit = SubmitField('Submit')
    reset = SubmitField('Reset', render_kw={"type": "reset"})

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=60)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=1, message='Age must be positive')])
    state_of_origin = StringField('State', validators=[Length(max=50)])
    submit = SubmitField('Sign Up')
    reset = SubmitField('Clear All', render_kw={"type": "reset"})

    def validate_email(self, email):
        """Check if the email is already taken
            First retrieve all the staffs,
            then check if there is a specific staff with that email
        """
        # staff = Staff.query.filter_by(email=email.data).first()
        all_staffs = storage.all(Staff).values()
        the_staff = ''
        for staff in all_staffs:
            staff_dict = staff.to_dict()
            if staff_dict['email'] == email.data:
                the_staff == staff
        if the_staff:
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