from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from grocery_app.config import Config
import os

# Initialize extensions without binding to a specific app
db = SQLAlchemy()
bcrypt = Bcrypt()

# Keep the existing app creation for compatibility
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt.init_app(app)