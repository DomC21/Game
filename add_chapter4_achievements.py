from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import models, schemas, crud

def add_chapter4_achievements():
    """
    Add special quiz achievements for Chapter 4.
    """
    # Create a database session
    db = SessionLocal()
    
    try:
        print("Adding special quiz achievements for Chapter 4...")
        
        # Get Chapter 4
        chapter = db.query(models.Chapter).filter(models.Chapter.title.like("%Chapter 4:%")).first()
        
        if not chapter:
            print("Error: Chapter 4 not found. Make sure the database is seeded.")
            return False
        
        print(f"Found Chapter: {chapter.title}")
        
        # Get the quiz for Chapter 4
        quiz = db.query(models.Quiz).filter(models.Quiz.chapter_id == chapter.id).first()
        
        if not quiz:
            print("Error: No quiz found for Chapter 4. Make sure the database is seeded.")
            return False
        
        print(f"Found Quiz: {quiz.title}")
        
        # Get all questions for this quiz
        questions = db.query(models.Question).filter(models.Question.quiz_id == quiz.id).all()
        
        if not questions:
            print("Error: No questions found for Chapter 4 quiz. Make sure the quiz is imported.")
            return False
        
        print(f"Found {len(questions)} questions for the quiz.")
        
        # Get the achievements for Chapter 4
        achievements = db.query(models.Achievement).filter(
            models.Achievement.chapter_id == chapter.id,
            models.Achievement.requirement_type == "special_quiz_achievement"
        ).all()
        
        if not achievements:
            print("Error: No special quiz achievements found for Chapter 4. Make sure the database is seeded.")
            return False
        
        print(f"Found {len(achievements)} special quiz achievements for Chapter 4.")
        
        # Create special quiz achievement requirements
        # Financial Detective: Questions about financial statements (1, 6, 8)
        # Valuation Virtuoso: Questions about valuation methods (3, 4, 9, 13, 19)
        # Moat Master: Questions about economic moats (5, 12, 15)
        
        # Map achievement titles to question IDs
        achievement_question_map = {
            "Financial Detective": [1, 6, 8],  # Financial statement questions
            "Valuation Virtuoso": [3, 4, 9, 13, 19],  # Valuation method questions
            "Moat Master": [5, 12, 15]  # Economic moat questions
        }
        
        # Create special quiz achievement requirements
        for achievement in achievements:
            if achievement.title in achievement_question_map:
                question_ids = achievement_question_map[achievement.title]
                
                # Get the actual question IDs from the database
                db_questions = []
                for i, q in enumerate(questions):
                    if i + 1 in question_ids:  # Question numbers are 1-indexed
                        db_questions.append(q)
                
                if not db_questions:
                    print(f"Warning: No matching questions found for achievement {achievement.title}.")
                    continue
                
                # Delete existing requirements for this achievement
                db.query(models.SpecialQuizAchievementRequirement).filter(
                    models.SpecialQuizAchievementRequirement.achievement_id == achievement.id
                ).delete()
                
                # Create new requirements
                for question in db_questions:
                    requirement = models.SpecialQuizAchievementRequirement(
                        achievement_id=achievement.id,
                        question_id=question.id
                    )
                    db.add(requirement)
                
                print(f"Added {len(db_questions)} question requirements for achievement: {achievement.title}")
        
        db.commit()
        print("Special quiz achievements for Chapter 4 added successfully!")
        return True
    
    finally:
        db.close()

if __name__ == "__main__":
    add_chapter4_achievements()
