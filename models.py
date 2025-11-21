from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    mail = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    date_registered = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    avatar = db.Column(db.String(255), nullable=True, default='default.png')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    author = db.relationship('Person', backref='posts')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    author = db.relationship('Person', backref='comments')
    post = db.relationship('Post', backref='comments')