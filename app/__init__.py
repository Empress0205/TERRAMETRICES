from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
db =SQLAlchemy()
csrf = CSRFProtect()


app = Flask(__name__)
csrf.init_app(app)

app.config.from_object('config.Config')

login_manager=LoginManager()

login_manager.init_app(app)
db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app import routes
from app.models import User
    