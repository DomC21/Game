from app.db import SessionLocal
from app.models import Achievement, Chapter

def add_chapter6_achievements():
    db = SessionLocal()
    try:
        # Get Chapter 6
        chapter6 = db.query(Chapter).filter(Chapter.title.like("%Chapter 6:%")).first()
        
        if not chapter6:
            print("Error: Chapter 6 not found in the database.")
            return False
            
        print(f"Found Chapter 6: {chapter6.title}")
        
        # Check if achievements already exist
        existing_achievements = db.query(Achievement).filter(Achievement.chapter_id == chapter6.id).all()
        if existing_achievements:
            print(f"Found {len(existing_achievements)} existing achievements for Chapter 6:")
            for achievement in existing_achievements:
                print(f"- {achievement.title}: {achievement.description}")
            return True
        
        # Create Chapter 6 achievements
        achievements = [
            {
                "title": "Risk Aware",
                "description": "Complete all 22 subsections with 80%+ on the quiz",
                "badge_image": "badge-risk-aware.png",
                "requirement_type": "quiz_score",
                "requirement_value": 80,
                "chapter_id": chapter6.id
            },
            {
                "title": "Drawdown Defender",
                "description": "Demonstrate strategies to limit your portfolio's maximum drawdown in a simulated environment",
                "badge_image": "badge-drawdown-defender.png",
                "requirement_type": "special_quiz_achievement",
                "requirement_value": 1,
                "chapter_id": chapter6.id
            },
            {
                "title": "Hedging Hero",
                "description": "Successfully apply a hedging technique (like buying puts or shorting an index) in a scenario-based mini-game",
                "badge_image": "badge-hedging-hero.png",
                "requirement_type": "special_quiz_achievement",
                "requirement_value": 1,
                "chapter_id": chapter6.id
            },
            {
                "title": "Kelly Cadet",
                "description": "Implement the Kelly Criterion in a practice scenario and compare results to a fixed fractional approach",
                "badge_image": "badge-kelly-cadet.png",
                "requirement_type": "special_quiz_achievement",
                "requirement_value": 1,
                "chapter_id": chapter6.id
            }
        ]
        
        # Add achievements to the database
        for achievement_data in achievements:
            achievement = Achievement(**achievement_data)
            db.add(achievement)
        
        db.commit()
        
        print(f"Successfully added {len(achievements)} achievements for Chapter 6.")
        return True
        
    except Exception as e:
        db.rollback()
        print(f"Error adding Chapter 6 achievements: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    add_chapter6_achievements()
