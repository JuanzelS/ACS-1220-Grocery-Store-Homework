# app.py
from grocery_app.extensions import app, db, login_manager
from grocery_app.models import User

# Configure user loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import and register blueprints ONLY HERE
from grocery_app.routes import main, auth
app.register_blueprint(main)
app.register_blueprint(auth)

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)