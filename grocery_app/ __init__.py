# grocery_app/__init__.py
from grocery_app.extensions import app, db, bcrypt, login_manager
from grocery_app.models import User, GroceryStore, GroceryItem

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Do NOT register blueprints here
# Do NOT create tables here