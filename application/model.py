from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):

    __tablename_ = "Table User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username, self.id)

    def hash_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Post(db.Model):
    __tablename_ = "Table Post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.Text, nullable=False)
    datepost = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False)

    def __repr__(self):
        return '<Content {}>'.format(self.id, self.title, self.datepost)


class Tag(db.Model):
    __tablename_ = "Tag Post"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    tag = db.relationship('Post', backref='tagname', lazy=True)
    

    def __repr__(self):
        return '<TagPost {}>'.format(self.id, self.name)


# class Comment(db.Model):

#     id = db.Column(db.Integer, primary_key=True)
#     Comment = db.Column(db.Text, nullable=False)
