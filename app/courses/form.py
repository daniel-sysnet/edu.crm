from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired, Length


class CourseForm(FlaskForm):

    title      = StringField("Titre du Cours",
                             validators=[DataRequired(), Length(min=2, max=200)])
    # teacher_id est rempli via la recherche par matricule
    teacher_id = HiddenField("Enseignant", validators=[DataRequired()])