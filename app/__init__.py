from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
db =SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/database.db'  # Path to your SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.config['SECRET_KEY'] ='your_secret_key_here'
login_manager=LoginManager()

login_manager.init_app(app)
db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app import routes
from app.models import User
    