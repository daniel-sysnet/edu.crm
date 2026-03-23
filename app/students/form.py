from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, DateField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional


class StudentForm(FlaskForm):

    name   = StringField("Nom Complet",
                         validators=[DataRequired(), Length(min=2, max=120)])
    gender = RadioField("Genre",
                        validators=[DataRequired()],
                        choices=[("M", "Masculin"), ("F", "Féminin")])
    dob    = DateField("Date de Naissance", validators=[Optional()])
    email  = EmailField("Adresse Email",
                        validators=[DataRequired(), Email()])
    phone  = StringField("Numéro de Téléphone",
                         validators=[DataRequired(), Length(min=9, max=9)])
    address = TextAreaField("Adresse Domicilière",
                            validators=[Optional(), Length(max=255)])