from app.db import SessionLocal
from app.models import Achievement

def check_achievements():
    db = SessionLocal()
    try:
        print("Checking achievements in the database...")
        achievements = db.query(Achievement).all()
        
        print(f"Found {len(achievements)} achievements:")
        for achievement in achievements:
            print(f"ID: {achievement.id}, Title: {achievement.title}, Type: {achievement.requirement_type}, Value: {achievement.requirement_value}, Chapter ID: {achievement.chapter_id}")
        
        # Check specifically for Foundations Master
        foundations_master = db.query(Achievement).filter(Achievement.title == "Foundations Master").first()
        if foundations_master:
            print("\nFoundations Master achievement details:")
            print(f"ID: {foundations_master.id}")
            print(f"Title: {foundations_master.title}")
            print(f"Description: {foundations_master.description}")
            print(f"Requirement Type: {foundations_master.requirement_type}")
            print(f"Requirement Value: {foundations_master.requirement_value}")
            print(f"Chapter ID: {foundations_master.chapter_id}")
        else:
            print("\nFoundations Master achievement not found in the database!")
    
    finally:
        db.close()

if __name__ == "__main__":
    check_achievements()
