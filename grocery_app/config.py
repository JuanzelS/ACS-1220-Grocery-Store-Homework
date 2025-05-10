"""Initialize Config class to access environment variables."""
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Config(object):
    """Set Flask configuration variables from environment variables."""
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-for-testing-only')
    
    # Ensure environment variables are set
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application")