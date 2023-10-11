from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/library'
db = SQLAlchemy(app)

from sweater import models, routes

with app.app_context():
     db.create_all()


# db.create_all()

# def create_app():
#     app = Flask(__name__)
#
#     with app.app_context():
#         db.create_all()
#
#     return app
