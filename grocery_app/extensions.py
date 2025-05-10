from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from grocery_app.config import Config
import os

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions with app
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

# Configure login manager
login_manager.login_view = 'auth.login'  # where to redirect for login
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'  # flash message category