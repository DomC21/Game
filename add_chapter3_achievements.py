from app.models import Achievement
from app.db import get_db

# Chapter 3 achievements
achievements = [
    {
        "title": "Chart Master",
        "description": "Complete all subsections in Chapter 3 and score at least 80% on the chapter quiz",
        "badge_image": "badge-chart-master.png",
        "requirement_type": "quiz_score",
        "requirement_value": 80,
        "chapter_id": 3
    },
    {
        "title": "Pattern Recognition Expert",
        "description": "Correctly identify all chart patterns in the Chapter 3 quiz",
        "badge_image": "badge-pattern-recognition.png",
        "requirement_type": "special_quiz_achievement",
        "requirement_value": 1,
        "chapter_id": 3
    },
    {
        "title": "Indicator Wizard",
        "description": "Complete all technical indicator exercises in the subsections",
        "badge_image": "badge-indicator-wizard.png",
        "requirement_type": "subsection_completion",
        "requirement_value": 20,
        "chapter_id": 3
    }
]

# Add achievements to the database
db = next(get_db())
try:
    print("Adding Chapter 3 achievements to the database...")
    
    # Check if achievements already exist
    existing_achievements = db.query(Achievement).filter(Achievement.chapter_id == 3).all()
    if existing_achievements:
        print(f"Found {len(existing_achievements)} existing Chapter 3 achievements:")
        for a in existing_achievements:
            print(f"- {a.title}: {a.description}")
        print("Skipping achievement creation.")
    else:
        # Add achievements to the database
        for achievement_data in achievements:
            achievement = Achievement(**achievement_data)
            db.add(achievement)
        
        # Commit the achievements
        db.commit()
        print("Chapter 3 achievements added successfully!")
        
        # Verify achievements were added
        added_achievements = db.query(Achievement).filter(Achievement.chapter_id == 3).all()
        print(f"Verified {len(added_achievements)} Chapter 3 achievements in database:")
        for a in added_achievements:
            print(f"- {a.title}: {a.description}")
finally:
    db.close()
