from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class CreateTag(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField('CreateTag')