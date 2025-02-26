import sys
import os
from sqlalchemy.orm import Session
from app import models, crud, schemas
from app.db import SessionLocal, engine

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

def test_chapter_completion():
    """
    Test the chapter completion functionality and the Foundations Master achievement.
    """
    # Create a database session
    db = SessionLocal()
    
    try:
        print("Starting Chapter 1 completion test...")
        
        # Create a test user
        test_user = schemas.UserCreate(
            email="test_user@example.com",
            username="test_user",
            password="password123"
        )
        
        # Check if user already exists
        existing_user = crud.get_user_by_email(db, test_user.email)
        if existing_user:
            print(f"User {test_user.email} already exists, using existing user.")
            user = existing_user
        else:
            print(f"Creating new test user: {test_user.email}")
            user = crud.create_user(db, test_user)
        
        print(f"Test user ID: {user.id}")
        
        # Get Chapter 1
        level = crud.get_level_by_number(db, 1)
        if not level:
            print("Error: Level 1 not found. Make sure the database is seeded.")
            return False
        
        chapters = crud.get_chapters_by_level(db, level.id)
        if not chapters:
            print("Error: No chapters found for Level 1. Make sure the database is seeded.")
            return False
        
        chapter = chapters[0]  # First chapter in Level 1
        print(f"Testing completion of Chapter: {chapter.title}")
        
        # Get all quizzes for Chapter 1
        quizzes = crud.get_quizzes_by_chapter(db, chapter.id)
        if not quizzes:
            print("Error: No quizzes found for Chapter 1. Make sure the database is seeded.")
            return False
        
        # Simulate completing all subsection quizzes with high scores
        print(f"Simulating completion of {len(quizzes)} quizzes...")
        
        for i, quiz in enumerate(quizzes):
            print(f"Completing quiz {i+1}/{len(quizzes)}: {quiz.title}")
            
            # Get all questions for this quiz
            questions = crud.get_questions_by_quiz(db, quiz.id)
            if not questions:
                print(f"Warning: No questions found for quiz {quiz.id}. Skipping.")
                continue
            
            # Create answers dict with all correct answers
            answers = {}
            for question in questions:
                # Find the correct option for this question
                correct_option = None
                for option in question.options:
                    if option.is_correct:
                        correct_option = option
                        break
                
                if correct_option:
                    answers[question.id] = correct_option.id
            
            # Submit the quiz with all correct answers
            result = crud.process_quiz_submission(db, user.id, quiz.id, answers)
            print(f"Quiz result: Score {result.score}/{result.max_score}, Points earned: {result.points_earned}")
            
            if result.new_achievements:
                print("New achievements earned:")
                for achievement in result.new_achievements:
                    print(f"  - {achievement.get('title')}: {achievement.get('description')}")
        
        # Check if user has earned the Foundations Master achievement
        user_achievements = crud.get_user_achievements(db, user.id)
        foundations_master_earned = False
        
        for user_achievement in user_achievements:
            achievement = crud.get_achievement(db, user_achievement.achievement_id)
            if achievement and achievement.title == "Foundations Master":
                foundations_master_earned = True
                print("\nSUCCESS: Foundations Master achievement earned!")
                break
        
        if not foundations_master_earned:
            print("\nFAILURE: Foundations Master achievement not earned.")
            
            # Check why the achievement wasn't earned
            all_achievements = crud.get_achievements(db)
            foundations_master = None
            
            for achievement in all_achievements:
                if achievement.title == "Foundations Master":
                    foundations_master = achievement
                    break
            
            if foundations_master:
                print(f"Foundations Master achievement details:")
                print(f"  - Requirement type: {foundations_master.requirement_type}")
                print(f"  - Requirement value: {foundations_master.requirement_value}")
                print(f"  - Chapter ID: {foundations_master.chapter_id}")
            else:
                print("Foundations Master achievement not found in the database.")
        
        # Check user's total points and level
        print(f"\nUser stats after completion:")
        print(f"  - Total points: {user.total_points}")
        print(f"  - Current level: {user.current_level}")
        
        return foundations_master_earned
    
    finally:
        db.close()

if __name__ == "__main__":
    success = test_chapter_completion()
    if success:
        print("\nTest passed: Chapter completion and Foundations Master achievement working correctly.")
        sys.exit(0)
    else:
        print("\nTest failed: Chapter completion or Foundations Master achievement not working correctly.")
        sys.exit(1)
