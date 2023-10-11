from datetime import datetime

from sweater import db


class Books(db.Model):
    __tablename__ = 'Books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    god_vipuska = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, title, god_vipuska):
        self.title = title
        self.god_vipuska = god_vipuska