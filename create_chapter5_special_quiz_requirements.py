from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import models, schemas, crud

def create_chapter5_special_quiz_requirements():
    """
    Create the special quiz achievement requirements for Chapter 5 achievements.
    """
    # Create a database session
    db = SessionLocal()
    
    try:
        print("Creating Chapter 5 special quiz achievement requirements...")
        
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
        
        # Get the achievements for Chapter 5
        achievements = db.query(models.Achievement).filter(
            models.Achievement.chapter_id == chapter.id,
            models.Achievement.requirement_type == "special_quiz_achievement"
        ).all()
        
        if not achievements:
            print("Error: No special quiz achievements found for Chapter 5.")
            return False
        
        print(f"Found {len(achievements)} special quiz achievements for Chapter 5.")
        
        # Get questions for the quiz
        questions = db.query(models.Question).filter(models.Question.quiz_id == quiz.id).all()
        
        if not questions:
            print("Error: No questions found for the quiz.")
            return False
        
        print(f"Found {len(questions)} questions for the quiz.")
        
        # Create special quiz achievement requirements for each achievement
        for achievement in achievements:
            print(f"Processing achievement: {achievement.title}")
            
            # For each achievement, create a requirement for each question
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
        print("Chapter 5 special quiz achievement requirements added successfully!")
        return True
    
    finally:
        db.close()

if __name__ == "__main__":
    create_chapter5_special_quiz_requirements()
