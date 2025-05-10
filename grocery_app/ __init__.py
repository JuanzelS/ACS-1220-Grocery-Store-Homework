from flask import Flask
from flask_login import LoginManager
from grocery_app.extensions import db, bcrypt
from grocery_app.config import Config

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database and bcrypt
db.init_app(app)
bcrypt.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from grocery_app.models import User
    return User.query.get(int(user_id))

# Register blueprints
with app.app_context():
    # Import routes
    from grocery_app.routes import main, auth
    
    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)
    
    # Create all database tables
    db.create_all()