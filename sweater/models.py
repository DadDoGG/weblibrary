from flask_login import UserMixin

from sweater import db, manager

class BaseIdModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)


class book(BaseIdModel):
    __tablename__ = 'book'
    title = db.Column(db.String(128), nullable=False)
    year_created = db.Column(db.Integer, nullable=False)

    user = db.relationship('user', secondary='book_user', back_populates='book')


class user(BaseIdModel, UserMixin):
    __tablename__ = 'user'
    email = db.Column(db.String(120), unique=True)
    surname = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(320), nullable=False)
    permission = db.Column(db.String(10), default="User")

    book = db.relationship('book', secondary='book_user', back_populates='user')

@manager.user_loader
def load_user(user_id):
    return user.query.get(user_id)


class book_user(db.Model):
    __tablename__ = 'book_user'
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

class menu(BaseIdModel):
    __tablename__ = 'menu'
    url = db.Column(db.String(120), unique=True)
    title = db.Column(db.String(120), unique=True)