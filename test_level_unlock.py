import sys
from sqlalchemy.orm import Session
from app import models, crud, schemas
from app.db import SessionLocal, engine

def test_level_unlock():
    """
    Test that a user can unlock Level 2 after earning 1,000 XP.
    """
    # Create a database session
    db = SessionLocal()
    
    try:
        print("Starting Level Unlock test...")
        
        # Create a test user
        test_user = schemas.UserCreate(
            email="level_test@example.com",
            username="level_test",
            password="password123"
        )
        
        # Check if user already exists
        existing_user = crud.get_user_by_email(db, test_user.email)
        if existing_user:
            print(f"User {test_user.email} already exists, using existing user.")
            user = existing_user
        else:
            print(f"Creating new test user: {test_user.email}")
            user = crud.create_user(db, test_user)
        
        print(f"Test user ID: {user.id}")
        
        # Get Level 1 and Level 2
        level1 = crud.get_level_by_number(db, 1)
        level2 = crud.get_level_by_number(db, 2)
        
        if not level1 or not level2:
            print("Error: Levels not found. Make sure the database is seeded.")
            return False
        
        print(f"Level 1: {level1.title}, Required XP: {level1.required_points}")
        print(f"Level 2: {level2.title}, Required XP: {level2.required_points}")
        
        # Check initial user level
        print(f"Initial user level: {user.current_level}")
        print(f"Initial user XP: {user.total_points}")
        
        # Add 1,000 XP to the user (enough to unlock Level 2)
        print(f"Adding 1,000 XP to user...")
        updated_user, level_up, new_level = crud.add_points_to_user(db, user.id, 1000)
        
        # Check if user leveled up
        print(f"User leveled up: {level_up}")
        if level_up:
            print(f"New level: {new_level}")
        
        # Check final user level
        print(f"Final user level: {updated_user.current_level}")
        print(f"Final user XP: {updated_user.total_points}")
        
        # Verify that Level 2 is now unlocked
        level2_unlocked = updated_user.current_level >= 2
        
        if level2_unlocked:
            print("\nSUCCESS: Level 2 unlocked successfully!")
        else:
            print("\nFAILURE: Level 2 was not unlocked.")
        
        return level2_unlocked
    
    finally:
        db.close()

if __name__ == "__main__":
    success = test_level_unlock()
    if success:
        print("\nTest passed: Level unlock functionality working correctly.")
        sys.exit(0)
    else:
        print("\nTest failed: Level unlock functionality not working correctly.")
        sys.exit(1)
