from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import IntegerField, StringField, SelectField, FileField, validators
from wtforms.validators import DataRequired

class PatientInfo(FlaskForm):
    Age = IntegerField(u'Age', validators=[DataRequired()])
    Gender = SelectField(u'Gender', choices=[('Male', 'Male'),('Female', 'Female')])
    Mole_location = SelectField(u'Mole_location', choices=[('Head', 'Head'),('Face', 'Face'),('Back', 'Back'),('Hand', 'Hand'),('Leg', 'Leg') ])
    Image = FileField(u'Image', validators=[FileRequired()])




