import os
from app.db import Base, engine
from app.seed_data import seed_data

def recreate_database():
    print("Recreating database with updated schema...")
    # Remove the database file if it exists
    if os.path.exists("trading_ebook.db"):
        os.remove("trading_ebook.db")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database schema recreated successfully.")
    
    # Seed the database
    print("Seeding the database...")
    seed_data()
    print("Database seeded successfully.")

if __name__ == "__main__":
    recreate_database()
