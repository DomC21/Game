from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import models

def add_missing_chapter4_achievements():
    """
    Add missing achievements for Chapter 4 to the database.
    """
    # Create a database session
    db = SessionLocal()
    
    try:
        print("Adding missing achievements for Chapter 4...")
        
        # Get Chapter 4
        chapter = db.query(models.Chapter).filter(models.Chapter.title.like("%Chapter 4:%")).first()
        
        if not chapter:
            print("Error: Chapter 4 not found. Make sure the database is seeded.")
            return False
        
        print(f"Found Chapter: {chapter.title}")
        
        # Define the achievements for Chapter 4
        achievements = [
            {
                "title": "Fundamentals Guru",
                "description": "Complete all 22 subsections in Chapter 4 and score at least 80% on the chapter quiz",
                "badge_image": "badge-fundamentals-guru.png",
                "requirement_type": "quiz_score",
                "requirement_value": 80,
                "chapter_id": chapter.id
            },
            {
                "title": "Financial Detective",
                "description": "Correctly identify the key takeaways from real companies' income statements and balance sheets",
                "badge_image": "badge-financial-detective.png",
                "requirement_type": "special_quiz_achievement",
                "requirement_value": 1,
                "chapter_id": chapter.id
            },
            {
                "title": "Valuation Virtuoso",
                "description": "Demonstrate proficiency in valuation methods by correctly answering all valuation-related questions",
                "badge_image": "badge-valuation-virtuoso.png",
                "requirement_type": "special_quiz_achievement",
                "requirement_value": 1,
                "chapter_id": chapter.id
            },
            {
                "title": "Moat Master",
                "description": "Correctly identify and analyze different types of economic moats",
                "badge_image": "badge-moat-master.png",
                "requirement_type": "special_quiz_achievement",
                "requirement_value": 1,
                "chapter_id": chapter.id
            }
        ]
        
        # Add achievements to the database
        for achievement_data in achievements:
            # Check if achievement already exists
            existing_achievement = db.query(models.Achievement).filter(
                models.Achievement.title == achievement_data["title"],
                models.Achievement.chapter_id == chapter.id
            ).first()
            
            if existing_achievement:
                print(f"Achievement already exists: {achievement_data['title']}")
            else:
                achievement = models.Achievement(**achievement_data)
                db.add(achievement)
                print(f"Added achievement: {achievement_data['title']}")
        
        db.commit()
        print("Missing achievements for Chapter 4 added successfully!")
        return True
    
    finally:
        db.close()

if __name__ == "__main__":
    add_missing_chapter4_achievements()
