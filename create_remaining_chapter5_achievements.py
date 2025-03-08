from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import models, schemas, crud

def create_remaining_chapter5_achievements():
    """
    Create the remaining Chapter 5 achievements in the database if they don't exist.
    """
    # Create a database session
    db = SessionLocal()
    
    try:
        print("Creating remaining Chapter 5 achievements...")
        
        # Get Chapter 5
        chapter = db.query(models.Chapter).filter(models.Chapter.title.like("%Chapter 5:%")).first()
        
        if not chapter:
            print("Error: Chapter 5 not found. Make sure the database is seeded.")
            return False
        
        print(f"Found Chapter: {chapter.title}")
        
        # Get the quiz for Chapter 5
        quiz = db.query(models.Quiz).filter(
            models.Quiz.title == "Portfolio Construction & Asset Allocation Quiz",
            models.Quiz.chapter_id == chapter.id
        ).first()
        
        if not quiz:
            print("Error: Quiz for Chapter 5 not found. Make sure the quiz is imported.")
            return False
        
        print(f"Found Quiz: {quiz.title}")
        
        # Define the remaining achievements for Chapter 5
        achievements = [
            {
                "title": "Rebalancing Ruler",
                "description": "Demonstrate the correct process of threshold rebalancing in a scenario-based mini-quiz",
                "badge_image": "badge-rebalancing-ruler.png",
                "requirement_type": "special_quiz_achievement",
                "requirement_value": 1,
                "chapter_id": chapter.id
            },
            {
                "title": "Policy Pro",
                "description": "Draft a personal Investment Policy Statement (IPS) and identify the key sections outlined in this chapter",
                "badge_image": "badge-policy-pro.png",
                "requirement_type": "special_quiz_achievement",
                "requirement_value": 1,
                "chapter_id": chapter.id
            }
        ]
        
        # Create or update the achievements
        for achievement_data in achievements:
            # Check if achievement already exists
            existing_achievement = db.query(models.Achievement).filter(
                models.Achievement.title == achievement_data["title"],
                models.Achievement.chapter_id == chapter.id
            ).first()
            
            if existing_achievement:
                print(f"Achievement {achievement_data['title']} already exists. Updating...")
                for key, value in achievement_data.items():
                    setattr(existing_achievement, key, value)
                achievement = existing_achievement
            else:
                print(f"Creating achievement: {achievement_data['title']}")
                achievement = models.Achievement(**achievement_data)
                db.add(achievement)
            
            db.commit()
            
            # Get questions for the quiz
            questions = db.query(models.Question).filter(models.Question.quiz_id == quiz.id).all()
            
            if not questions:
                print("Error: No questions found for the quiz.")
                return False
            
            print(f"Found {len(questions)} questions for the quiz.")
            
            # For each achievement, create a requirement for each question
            print(f"Processing achievement: {achievement.title}")
            
            for question in questions:
                # Check if requirement already exists
                existing_req = db.query(models.SpecialQuizAchievementRequirement).filter(
                    models.SpecialQuizAchievementRequirement.achievement_id == achievement.id,
                    models.SpecialQuizAchievementRequirement.question_id == question.id
                ).first()
                
                if existing_req:
                    print(f"Requirement for {achievement.title} and question {question.id} already exists. Skipping.")
                    continue
                
                # Create the requirement
                requirement = models.SpecialQuizAchievementRequirement(
                    achievement_id=achievement.id,
                    question_id=question.id
                )
                
                db.add(requirement)
                print(f"Added requirement for {achievement.title} and question {question.id}")
        
        db.commit()
        print("Remaining Chapter 5 achievements created successfully!")
        return True
    
    finally:
        db.close()

if __name__ == "__main__":
    create_remaining_chapter5_achievements()
