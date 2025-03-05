from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Achievement

def check_achievements():
    """
    Check if the Chapter 2 achievements are properly added to the database.
    """
    # Create a database session
    db = SessionLocal()
    
    try:
        # Get all achievements
        achievements = db.query(Achievement).all()
        
        print(f"Found {len(achievements)} achievements:")
        
        # Print details of all achievements
        for achievement in achievements:
            print(f"ID: {achievement.id}, Title: {achievement.title}, Type: {achievement.requirement_type}, Value: {achievement.requirement_value}, Chapter ID: {achievement.chapter_id}")
        
        # Check for Chapter 2 achievements
        chapter2_achievements = [
            ("Psychology Expert", "quiz_score", 80, 2),
            ("Emotional Mastery", "subsection_completion", 22, 2),
            ("Bias Buster", "special_quiz_achievement", 1, 2)
        ]
        
        print("\nVerifying Chapter 2 achievements:")
        
        for title, req_type, req_value, chapter_id in chapter2_achievements:
            achievement = db.query(Achievement).filter(
                Achievement.title == title,
                Achievement.requirement_type == req_type,
                Achievement.requirement_value == req_value,
                Achievement.chapter_id == chapter_id
            ).first()
            
            if achievement:
                print(f"✅ Found achievement: {title} (Type: {req_type}, Value: {req_value}, Chapter ID: {chapter_id})")
            else:
                print(f"❌ Missing achievement: {title} (Type: {req_type}, Value: {req_value}, Chapter ID: {chapter_id})")
    
    finally:
        db.close()

if __name__ == "__main__":
    check_achievements()
