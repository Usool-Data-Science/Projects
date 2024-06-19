from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField,
                     IntegerField, SelectField, BooleanField, TelField)
from wtforms.validators import (DataRequired, Email, EqualTo,
                                Length, NumberRange, ValidationError)

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
