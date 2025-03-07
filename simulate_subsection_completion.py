from app.models import UserProgress
from app.db import get_db

def simulate_subsection_completion():
    """
    Simulate completing all subsections for Chapter 3 for the test user.
    """
    db = next(get_db())
    try:
        print("Simulating completion of all Chapter 3 subsections...")
        
        # Get the test user ID
        user_id = 5  # This is the test user ID from test_chapter3_completion.py
        
        # Get Chapter 3 ID
        chapter_id = 3
        
        # Simulate completing all 22 subsections
        for i in range(1, 23):
            subsection_id = f"3_{i}"
            
            # Check if progress already exists
            existing_progress = db.query(UserProgress).filter(
                UserProgress.user_id == user_id,
                UserProgress.subsection_id == subsection_id
            ).first()
            
            if existing_progress:
                print(f"Subsection {subsection_id} already completed. Skipping.")
                continue
            
            # Create progress record
            progress = UserProgress(
                user_id=user_id,
                subsection_id=subsection_id,
                is_completed=True,
                points_earned=50  # Award 50 points per subsection
            )
            db.add(progress)
        
        # Commit the changes
        db.commit()
        print("All Chapter 3 subsections completed successfully!")
        
    finally:
        db.close()

if __name__ == "__main__":
    simulate_subsection_completion()
