from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import models, schemas, crud

def test_chapter3_completion():
    """
    Test the Chapter 3 completion functionality and the Chapter 3 achievements.
    """
    # Create a database session
    db = SessionLocal()
    
    try:
        print("Starting Chapter 3 completion test...")
        
        # Create a test user
        test_user = schemas.UserCreate(
            email="test_user_ch3@example.com",
            username="test_user_ch3",
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
        
        # Get Chapter 3
        chapter = db.query(models.Chapter).filter(models.Chapter.title.like("%Chapter 3:%")).first()
        
        if not chapter:
            print("Error: Chapter 3 not found. Make sure the database is seeded.")
            return False
        
        print(f"Testing completion of Chapter: {chapter.title}")
        
        # Get all quizzes for Chapter 3
        quizzes = crud.get_quizzes_by_chapter(db, chapter.id)
        if not quizzes:
            print("Error: No quizzes found for Chapter 3. Make sure the database is seeded.")
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
        
        # Check if user has earned the Chart Master achievement
        user_achievements = crud.get_user_achievements(db, user.id)
        chart_master_earned = False
        pattern_expert_earned = False
        indicator_wizard_earned = False
        
        for user_achievement in user_achievements:
            achievement = crud.get_achievement(db, user_achievement.achievement_id)
            if achievement:
                if achievement.title == "Chart Master":
                    chart_master_earned = True
                    print("\nSUCCESS: Chart Master achievement earned!")
                elif achievement.title == "Pattern Recognition Expert":
                    pattern_expert_earned = True
                    print("\nSUCCESS: Pattern Recognition Expert achievement earned!")
                elif achievement.title == "Indicator Wizard":
                    indicator_wizard_earned = True
                    print("\nSUCCESS: Indicator Wizard achievement earned!")
        
        if not chart_master_earned:
            print("\nFAILURE: Chart Master achievement not earned.")
        
        if not pattern_expert_earned:
            print("\nFAILURE: Pattern Recognition Expert achievement not earned.")
        
        if not indicator_wizard_earned:
            print("\nFAILURE: Indicator Wizard achievement not earned.")
        
        # Return True if all achievements were earned
        all_achievements_earned = chart_master_earned and pattern_expert_earned and indicator_wizard_earned
        
        if all_achievements_earned:
            print("\nAll Chapter 3 achievements earned successfully!")
        else:
            print("\nNot all Chapter 3 achievements were earned.")
        
        return all_achievements_earned
    
    finally:
        db.close()

if __name__ == "__main__":
    success = test_chapter3_completion()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")
