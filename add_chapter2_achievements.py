from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Achievement

def add_chapter2_achievements():
    """
    Add Chapter 2 achievements to the database.
    """
    # Create a database session
    db = SessionLocal()
    
    try:
        # Chapter 2 achievements
        chapter2_achievements = [
            {
                "title": "Psychology Expert",
                "description": "Complete all subsections in Chapter 2 and score at least 80% on the chapter quiz",
                "badge_image": "badge-psychology-expert.png",
                "requirement_type": "quiz_score",
                "requirement_value": 80,
                "chapter_id": 2
            },
            {
                "title": "Emotional Mastery",
                "description": "Complete the emotional self-assessment exercises in all subsections",
                "badge_image": "badge-emotional-mastery.png",
                "requirement_type": "subsection_completion",
                "requirement_value": 22,
                "chapter_id": 2
            },
            {
                "title": "Bias Buster",
                "description": "Correctly identify all cognitive biases in the Chapter 2 quiz",
                "badge_image": "badge-bias-buster.png",
                "requirement_type": "special_quiz_achievement",
                "requirement_value": 1,
                "chapter_id": 2
            }
        ]
        
        # Check if each achievement already exists, add if not
        for achievement_data in chapter2_achievements:
            existing = db.query(Achievement).filter(
                Achievement.title == achievement_data["title"],
                Achievement.requirement_type == achievement_data["requirement_type"],
                Achievement.chapter_id == achievement_data["chapter_id"]
            ).first()
            
            if existing:
                print(f"Achievement already exists: {achievement_data['title']}")
            else:
                achievement = Achievement(**achievement_data)
                db.add(achievement)
                print(f"Added achievement: {achievement_data['title']}")
        
        db.commit()
        print("Chapter 2 achievements added successfully!")
    
    finally:
        db.close()

if __name__ == "__main__":
    add_chapter2_achievements()
