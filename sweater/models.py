from datetime import datetime

from sweater import db


class Books(db.Model):
    __tablename__ = 'Books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    god_vipuska = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    authors = db.relationship('Authors', secondary='Relation', back_populates='books')

    def __init__(self, title, god_vipuska):
        self.title = title
        self.god_vipuska = god_vipuska


class Authors(db.Model):
    __tablename__ = 'Authors'
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(32), nullable=False)
    initials = db.Column(db.String(32), nullable=False)

    books = db.relationship('Books', secondary='Relation', back_populates='authors')
    def __init__(self, surname, initials):
        self.surname = surname
        self.initials = initials

class Relation(db.Model):
    __tablename__ = 'Relation'
    book_id = db.Column(db.Integer, db.ForeignKey('Books.id'), primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('Authors.id'), primary_key=True)