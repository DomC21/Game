import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import SpecialQuizAchievementRequirement, Achievement, Question, Quiz, Chapter
from app.db import Base

# Set up database connection
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./trading_ebook.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_special_quiz_requirements():
    db = SessionLocal()
    try:
        # Get Chapter 6
        chapter6 = db.query(Chapter).filter(Chapter.title.like("%Chapter 6:%")).first()
        
        if not chapter6:
            print("Error: Chapter 6 not found in the database.")
            return
            
        print(f"Found Chapter 6: {chapter6.title}")
        
        # Get Chapter 6 quiz
        quiz = db.query(Quiz).filter(Quiz.chapter_id == chapter6.id).first()
        
        if not quiz:
            print("Error: Quiz for Chapter 6 not found in the database.")
            return
            
        print(f"Found quiz: {quiz.title}")
        
        # Get Chapter 6 achievements
        risk_aware = db.query(Achievement).filter(
            Achievement.title == "Risk Aware",
            Achievement.chapter_id == chapter6.id
        ).first()
        
        drawdown_defender = db.query(Achievement).filter(
            Achievement.title == "Drawdown Defender",
            Achievement.chapter_id == chapter6.id
        ).first()
        
        hedging_hero = db.query(Achievement).filter(
            Achievement.title == "Hedging Hero",
            Achievement.chapter_id == chapter6.id
        ).first()
        
        kelly_cadet = db.query(Achievement).filter(
            Achievement.title == "Kelly Cadet",
            Achievement.chapter_id == chapter6.id
        ).first()
        
        if not all([risk_aware, drawdown_defender, hedging_hero, kelly_cadet]):
            print("Error: Not all Chapter 6 achievements found in the database.")
            missing = []
            if not risk_aware:
                missing.append("Risk Aware")
            if not drawdown_defender:
                missing.append("Drawdown Defender")
            if not hedging_hero:
                missing.append("Hedging Hero")
            if not kelly_cadet:
                missing.append("Kelly Cadet")
            print(f"Missing achievements: {', '.join(missing)}")
            return
        
        print("Found all Chapter 6 achievements.")
        
        # Get questions for Chapter 6 quiz
        questions = db.query(Question).filter(Question.quiz_id == quiz.id).all()
        
        if not questions:
            print("Error: No questions found for Chapter 6 quiz.")
            return
        
        print(f"Found {len(questions)} questions for Chapter 6 quiz.")
        
        # Map question numbers to question IDs
        question_map = {i+1: q.id for i, q in enumerate(questions)}
        
        # Create special quiz requirements for each achievement
        requirements = []
        
        # Risk Aware - Complete all 22 subsections with 80%+ on the quiz
        # For this achievement, we'll use the first question as a placeholder
        if len(questions) > 0:
            risk_aware_req = SpecialQuizAchievementRequirement(
                achievement_id=risk_aware.id,
                question_id=questions[0].id
            )
            requirements.append(risk_aware_req)
        
        # Drawdown Defender - Demonstrate strategies to limit drawdown
        # Questions about drawdown, stress testing, and risk management
        drawdown_question_nums = [5, 9, 12]
        for q_num in drawdown_question_nums:
            if q_num <= len(questions):
                req = SpecialQuizAchievementRequirement(
                    achievement_id=drawdown_defender.id,
                    question_id=questions[q_num-1].id
                )
                requirements.append(req)
        
        # Hedging Hero - Successfully apply hedging techniques
        # Questions about hedging, correlation, and leverage
        # Since we only have 7 questions imported, we'll use the ones we have
        hedging_question_nums = [1, 4, 7]  # Use questions that exist in our database
        for q_num in hedging_question_nums:
            if q_num <= len(questions):
                req = SpecialQuizAchievementRequirement(
                    achievement_id=hedging_hero.id,
                    question_id=questions[q_num-1].id
                )
                requirements.append(req)
        
        # Kelly Cadet - Implement Kelly Criterion
        # Questions about Kelly Criterion, position sizing, and risk-reward
        kelly_question_nums = [3, 6, 13]
        for q_num in kelly_question_nums:
            if q_num <= len(questions):
                req = SpecialQuizAchievementRequirement(
                    achievement_id=kelly_cadet.id,
                    question_id=questions[q_num-1].id
                )
                requirements.append(req)
        
        # Add requirements to database
        for req in requirements:
            db.add(req)
        db.commit()
        
        print(f"Successfully created {len(requirements)} special quiz requirements for Chapter 6 achievements.")
        
    except Exception as e:
        db.rollback()
        print(f"Error creating special quiz requirements: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_special_quiz_requirements()
