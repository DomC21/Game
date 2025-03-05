import os
from app.db import Base, engine
from app import models
from app.seed_data import seed_data

def setup_database():
    """
    Recreate the database and seed it with initial data.
    """
    print("Setting up the database...")
    
    # Remove the database file if it exists
    if os.path.exists("trading_ebook.db"):
        print("Removing existing database...")
        os.remove("trading_ebook.db")
    
    # Create all tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Seed the database
    print("Seeding the database...")
    seed_data()
    
    print("Database setup complete!")

if __name__ == "__main__":
    setup_database()
