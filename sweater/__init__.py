from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfgdfg23423j2bf3kj2lh34g54t'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://test1:123@localhost/library'
db = SQLAlchemy(app)
manager = LoginManager(app)
manager.login_view = 'login'
manager.login_message = "Авторизуйтесь для доступа к странице"
manager.login_message_category = "success"


from sweater import models, routes

with app.app_context():
     db.create_all()


