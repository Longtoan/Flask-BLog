from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from ..model import Tag


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])

    content = TextAreaField('Content', validators=[DataRequired()])
    tag = SelectField('Tag', choices=[])
    submit = SubmitField('Post')
