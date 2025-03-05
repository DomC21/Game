from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import models, schemas, crud

def test_chapter2_completion():
    """
    Test the Chapter 2 completion functionality and the Psychology Expert achievement.
    """
    # Create a database session
    db = SessionLocal()
    
    try:
        print("Starting Chapter 2 completion test...")
        
        # Create a test user
        test_user = schemas.UserCreate(
            email="test_user_ch2@example.com",
            username="test_user_ch2",
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
        
        # Get Chapter 2
        chapter = db.query(models.Chapter).filter(models.Chapter.title.like("%Chapter 2:%")).first()
        
        if not chapter:
            print("Error: Chapter 2 not found. Make sure the database is seeded.")
            return False
        
        print(f"Testing completion of Chapter: {chapter.title}")
        
        # Get all quizzes for Chapter 2
        quizzes = crud.get_quizzes_by_chapter(db, chapter.id)
        if not quizzes:
            print("Error: No quizzes found for Chapter 2. Make sure the database is seeded.")
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
        
        # Check if user has earned the Psychology Expert achievement
        user_achievements = crud.get_user_achievements(db, user.id)
        psychology_expert_earned = False
        
        for user_achievement in user_achievements:
            achievement = crud.get_achievement(db, user_achievement.achievement_id)
            if achievement and achievement.title == "Psychology Expert":
                psychology_expert_earned = True
                print("\nSUCCESS: Psychology Expert achievement earned!")
        
        if not psychology_expert_earned:
            print("\nFAILURE: Psychology Expert achievement not earned.")
        
        # Check if user has earned the Emotional Mastery achievement
        emotional_mastery_earned = False
        for user_achievement in user_achievements:
            achievement = crud.get_achievement(db, user_achievement.achievement_id)
            if achievement and achievement.title == "Emotional Mastery":
                emotional_mastery_earned = True
                print("\nSUCCESS: Emotional Mastery achievement earned!")
        
        if not emotional_mastery_earned:
            print("\nFAILURE: Emotional Mastery achievement not earned.")
        
        # Check if user has earned the Bias Buster achievement
        bias_buster_earned = False
        for user_achievement in user_achievements:
            achievement = crud.get_achievement(db, user_achievement.achievement_id)
            if achievement and achievement.title == "Bias Buster":
                bias_buster_earned = True
                print("\nSUCCESS: Bias Buster achievement earned!")
        
        if not bias_buster_earned:
            print("\nFAILURE: Bias Buster achievement not earned.")
        
        return psychology_expert_earned and emotional_mastery_earned and bias_buster_earned
    
    finally:
        db.close()

if __name__ == "__main__":
    test_chapter2_completion()
