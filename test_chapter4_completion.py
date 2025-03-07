from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import models, schemas, crud

def test_chapter4_completion():
    """
    Test the Chapter 4 completion functionality and the achievements.
    """
    # Create a database session
    db = SessionLocal()
    
    try:
        print("Starting Chapter 4 completion test...")
        
        # Create a test user
        test_user = schemas.UserCreate(
            email="test_user_ch4@example.com",
            username="test_user_ch4",
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
        
        # Get Chapter 4
        chapter = db.query(models.Chapter).filter(models.Chapter.title.like("%Chapter 4:%")).first()
        
        if not chapter:
            print("Error: Chapter 4 not found. Make sure the database is seeded.")
            return False
        
        print(f"Testing completion of Chapter: {chapter.title}")
        
        # Get all quizzes for Chapter 4
        quizzes = crud.get_quizzes_by_chapter(db, chapter.id)
        if not quizzes:
            print("Error: No quizzes found for Chapter 4. Make sure the database is seeded.")
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
                    print(f"  - {achievement.title}: {achievement.description}")
        
        # Check if user has earned all Chapter 4 achievements
        user_achievements = crud.get_user_achievements(db, user.id)
        all_achievements_earned = True
        
        # List of expected Chapter 4 achievements
        expected_achievements = ["Fundamentals Guru", "Financial Detective", "Valuation Virtuoso", "Moat Master"]
        
        # Check each expected achievement
        for achievement_title in expected_achievements:
            achievement_earned = False
            for user_achievement in user_achievements:
                achievement = crud.get_achievement(db, user_achievement.achievement_id)
                if achievement and achievement.title == achievement_title:
                    achievement_earned = True
                    print(f"\nSUCCESS: {achievement_title} achievement earned!")
                    break
            
            if not achievement_earned:
                print(f"\nFAILURE: {achievement_title} achievement not earned.")
                all_achievements_earned = False
        
        return all_achievements_earned
    
    finally:
        db.close()

if __name__ == "__main__":
    success = test_chapter4_completion()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")
