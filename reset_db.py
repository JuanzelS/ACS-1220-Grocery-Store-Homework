# reset_db.py
import os
import shutil
from pathlib import Path

# First, search for all .db files to help us identify where the database is
print("Searching for .db files...")
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.db'):
            db_path = os.path.join(root, file)
            print(f"Found database file: {db_path}")
            try:
                os.remove(db_path)
                print(f"Successfully deleted: {db_path}")
            except Exception as e:
                print(f"Failed to delete {db_path}: {e}")

# Now import our app and models
from grocery_app.extensions import app, db
from grocery_app.models import User, GroceryStore, GroceryItem

with app.app_context():
    # Print the database URI from app config
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    print(f"Database URI: {db_uri}")
    
    # If using SQLite, get the database path
    if db_uri.startswith('sqlite:///'):
        db_path = db_uri.replace('sqlite:///', '')
        # Check if the path is relative or absolute
        if not os.path.isabs(db_path):
            # If relative, make it absolute
            abs_db_path = os.path.join(os.getcwd(), db_path)
        else:
            abs_db_path = db_path
        print(f"Absolute database path: {abs_db_path}")
        
        # Make sure the directory exists
        os.makedirs(os.path.dirname(abs_db_path) or '.', exist_ok=True)
        
        # Delete the file if it exists
        if os.path.exists(abs_db_path):
            try:
                os.remove(abs_db_path)
                print(f"Deleted database file: {abs_db_path}")
            except Exception as e:
                print(f"Failed to delete {abs_db_path}: {e}")
    
    # Drop all tables (in case the database exists)
    try:
        db.drop_all()
        print("Successfully dropped all tables")
    except Exception as e:
        print(f"Error dropping tables: {e}")
    
    # Create all tables with the new schema
    try:
        db.create_all()
        print("Successfully created all tables with the new schema")
    except Exception as e:
        print(f"Error creating tables: {e}")
    
    # List all tables in the database
    tables = db.engine.table_names()
    print(f"Tables created: {tables}")
    
    # Check columns in each table
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    
    for table in tables:
        columns = inspector.get_columns(table)
        column_names = [col['name'] for col in columns]
        print(f"Columns in {table} table: {column_names}")
    
    print("Database reset completed!")