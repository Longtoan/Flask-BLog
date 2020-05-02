from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegisterFormValidation(FlaskForm):
    username = StringField('username', validators=[
                           DataRequired(), Length(min=5, max=20)])

    email = StringField('email', validators=[
                        DataRequired(), Email(message='Please enter a valid email')])

    password = PasswordField('password', validators=[
                             DataRequired(), Length(min=6, message="Please select a password strongers")])

    password_comfirm = PasswordField('password_comfirm', validators=[
        DataRequired(), EqualTo('password', message="Password must match")])

    submit = SubmitField('signup')


class LoginFormValidation(FlaskForm):
    email = StringField('email', validators=[
        Email(message='Please enter a valid email')])

    password = PasswordField('password', validators=[
                           DataRequired()])

    submit = SubmitField('Login')
