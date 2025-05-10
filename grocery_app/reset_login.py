# reset_login.py
from grocery_app.extensions import app, db, bcrypt
from flask_login import LoginManager
from grocery_app.models import User

print("Setting up Flask-Login...")

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

print("Flask-Login setup complete!")

# Test if the login_manager is properly initialized
print(f"login_manager initialized: {login_manager is not None}")
print(f"login_manager.app: {login_manager.app is not None}")