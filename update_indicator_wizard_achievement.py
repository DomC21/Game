from app.models import Achievement
from app.db import get_db

def update_indicator_wizard_achievement():
    """
    Update the Indicator Wizard achievement to use the correct requirement type.
    """
    db = next(get_db())
    try:
        print("Updating Indicator Wizard achievement...")
        
        # Get the Indicator Wizard achievement
        achievement = db.query(Achievement).filter(
            Achievement.title == "Indicator Wizard",
            Achievement.chapter_id == 3
        ).first()
        
        if not achievement:
            print("Error: Indicator Wizard achievement not found.")
            return False
        
        print(f"Found achievement: {achievement.title}")
        print(f"Current requirement_type: {achievement.requirement_type}")
        print(f"Current requirement_value: {achievement.requirement_value}")
        
        # Update the achievement to use special_quiz_achievement
        achievement.requirement_type = "special_quiz_achievement"
        achievement.requirement_value = 1
        
        # Commit the changes
        db.commit()
        
        # Verify the update
        updated_achievement = db.query(Achievement).filter(
            Achievement.title == "Indicator Wizard",
            Achievement.chapter_id == 3
        ).first()
        
        print(f"Updated requirement_type: {updated_achievement.requirement_type}")
        print(f"Updated requirement_value: {updated_achievement.requirement_value}")
        
        print("Indicator Wizard achievement updated successfully!")
        return True
    
    finally:
        db.close()

if __name__ == "__main__":
    update_indicator_wizard_achievement()
