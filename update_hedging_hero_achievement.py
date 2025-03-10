from app.db import SessionLocal
from app.models import Achievement, Chapter

def update_hedging_hero_achievement():
    db = SessionLocal()
    try:
        # Get Chapter 6
        chapter6 = db.query(Chapter).filter(Chapter.title.like("%Chapter 6:%")).first()
        
        if not chapter6:
            print("Error: Chapter 6 not found in the database.")
            return False
            
        print(f"Found Chapter 6: {chapter6.title}")
        
        # Get Hedging Hero achievement
        hedging_hero = db.query(Achievement).filter(
            Achievement.title == "Hedging Hero",
            Achievement.chapter_id == chapter6.id
        ).first()
        
        if not hedging_hero:
            print("Error: Hedging Hero achievement not found in the database.")
            return False
            
        print(f"Found Hedging Hero achievement: {hedging_hero.title}")
        print(f"Current requirement type: {hedging_hero.requirement_type}")
        print(f"Current requirement value: {hedging_hero.requirement_value}")
        
        # Update the achievement to use quiz_score requirement type
        hedging_hero.requirement_type = "quiz_score"
        hedging_hero.requirement_value = 80
        
        db.commit()
        
        print(f"Updated Hedging Hero achievement:")
        print(f"New requirement type: {hedging_hero.requirement_type}")
        print(f"New requirement value: {hedging_hero.requirement_value}")
        
        return True
        
    except Exception as e:
        db.rollback()
        print(f"Error updating Hedging Hero achievement: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    update_hedging_hero_achievement()
