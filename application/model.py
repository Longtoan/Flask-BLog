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
    posts = db.relationship('CreatePost', backref='author', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username,self.id )

    def hash_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)


class CreatePost(db.Model):
    __tablename_ = "Table Content"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    # Tag = db.Column(db.String(50), unique=False, nullable=False)
    content = db.Column(db.Text, nullable=False)
    datepost = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Content {}>'.format(self.id,self.title, self.datepost)
