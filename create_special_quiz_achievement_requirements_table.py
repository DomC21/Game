from sqlalchemy.orm import Session
from app.db import SessionLocal, engine
from app import models

def create_special_quiz_achievement_requirements_table():
    """
    Create the special_quiz_achievement_requirements table in the database.
    """
    print("Creating special_quiz_achievement_requirements table...")
    
    # Create the table
    models.Base.metadata.create_all(bind=engine)
    
    print("Table created successfully!")
    return True

if __name__ == "__main__":
    create_special_quiz_achievement_requirements_table()
