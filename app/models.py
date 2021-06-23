from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager

# User object

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True)
    email = db.Column(db.String, unique=True, index=True)
    pass_secure = db.Column(db.String(255))
    posts = db.relationship('Post', backref='user', lazy="dynamic")
    comments = db.relationship('Comment', backref='user', lazy="dynamic")

    def __repr__(self):
        return f'User {self.username}'

    @property
    def password(self):
        raise AttributeError('You cannot raise the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    # save user
    def save_user(self):
        db.session.add(self)
        db.session.commit()


# Post object


class Post(db.Model):
    __tablename__ = 'posts'
    __searchable__ = ['title']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    likes = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy="dynamic")

    def __repr__(self):
        return f'Post {self.title}'

    def __init__(self, user_id, title, content, likes=0):
        self.user_id = user_id
        self.title = title
        self.content = content
        self.likes = likes

    # save post
    def save_post(self):
        db.session.add(self)
        db.session.commit()

    # getting posts
    @classmethod
    def get_all_posts(cls):
        posts = Post.query.all()
        return posts

    @classmethod
    def user_specific_posts(cls, id):
        posts = Post.query.filter_by(user_id = id).all()
        return posts

    @classmethod
    def search_post(cls,post_name):
        posts = Post.query.filter_by(title = post_name).all()
        return posts

    @classmethod
    def delete_post(cls, id):
        post  = Post.query.filter_by(id = id).first()
        db.session.delete(post)
        db.session.commit()


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key =True)
    comment = db.Column(db.String)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, user_id, post_id, comment):
        self.user_id = user_id
        self.post_id = post_id
        self.comment = comment

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_post_specific_comment(cls, id):
        comments = Comment.query.filter_by(post_id = id).all()
        return comments