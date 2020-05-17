from flask import request, jsonify, render_template, make_response, redirect, url_for, flash
from flask_login import login_required, logout_user, current_user, login_user, login_required
from datetime import datetime as data
from flask import current_app as app
from .model import db, User, Post, Tag
from .validation.account import RegisterFormValidation, LoginFormValidation, UpdateProfile
from .validation.CreatePost import PostForm
from .validation.createTag import CreateTag
from .import login_manager
from sqlalchemy import exc


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    tags = Tag.query.all()
    return render_template('home.html', title="Home", posts=posts,tags=tags)


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
    return render_template('register.html', title="Register", form=register)


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
    return render_template('login.html', title="Login ", form=login)


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    image_file = url_for('static', filename='profile/' +
                         current_user.image_file)
    posts = Post.query.filter_by(user_id=current_user.id).all()
    # for i in posts:
    #     print(i.title)
    return render_template("account.html", title="Account", image_file=image_file, posts=posts)


@app.route("/setting")
@login_required
def setting():
    form = UpdateProfile()
    if form.validate_on_submit():
        username = form.get.data
        user = User.query.filter_by(username=username).first()
        if(user is None):
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('account'))
    return render_template("accountSetting.html", title="Account Setting", form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def createpost():
    postform = PostForm()
    postform.tag.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
    # print(postform.tag.choices)

    if request.method == "POST":
        # print(form.tag.data)
        title = postform.title.data
        content = postform.content.data
        tag = Tag.query.filter_by(id=postform.tag.data).first()
        post = Post(title=title, content=content,
                    author=current_user, tagname=tag)
        # print(post)
        try:
            db.session.add(post)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            print(e)
        db.session.rollback()
        db.session.flush()

        return redirect(url_for("home"))
    print(request.form)
    return render_template("createpost.html", title="New Post", form=postform)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('post.html', title=post.title, post=post)


# @app.route("/taglist")
# def taglist():
#     tag = Tag.query.all()
#     return render_template("taglist.html", title="TagList", tag=tag)

@app.route("/taglist/<int:post_id>")
def tag(tag_id):
    tag = Tag.query.query_or_404(tag_id)
    return render_template("taglist.html", title="tag", tag=tag)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/createTag", methods=['GET', 'POST'])
def createTag():
    createTag = CreateTag()
    if createTag.validate_on_submit():
        name = createTag.name.data
        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("createtag.html", title="Create Tag", form=createTag)


@login_manager.user_loader
def load_user(user_id):

    if user_id is not None:
        return User.query.get(user_id)
    return None
