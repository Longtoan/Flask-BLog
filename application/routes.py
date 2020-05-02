from flask import request, jsonify, render_template, make_response, redirect, url_for, flash
from flask_login import login_required, logout_user, current_user, login_user, login_required
from datetime import datetime as data
from flask import current_app as app
from .model import db, User
from .validation.form import RegisterFormValidation, LoginFormValidation
from .import login_manager


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    register = RegisterFormValidation()

    if register.validate_on_submit():
        username = register.username.data
        email = register.email.data
        password = register.password.data
        existing_email = User.query.filter_by(
            email=email).first()  # check if user exists
        if(existing_email is None):
            user = User(username=username, email=email, password=password)
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('home'))
        else:

            flash("A user already exists with that email or username")
    return render_template('register.html', form=register)


@app.route("/login", methods=['GET', 'POST'])
def login():

    login = LoginFormValidation()
    if login.validate_on_submit():
        email = login.email.data
        password = login.password.data
        user = User.query.filter_by(email=email).first()

        if(user and user.check_password(password=password)):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Invalid email/password combination')
    return render_template('login.html', form=login)


@app.route("/account")
@login_required
def account():
    image_file = url_for('static', filename='profile/' + current_user.image_file)
    return render_template("account.html",image_file=image_file)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@login_manager.user_loader
def load_user(user_id):

    if user_id is not None:
        return User.query.get(user_id)
    return None
