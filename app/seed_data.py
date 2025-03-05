import sys
import os
from sqlalchemy.orm import Session
import app.crud as crud
import app.models as models
import app.schemas as schemas
from app.db import SessionLocal, engine

def seed_data():
    """
    Seed the database with initial data.
    """
    # Create tables if they don't exist
    models.Base.metadata.create_all(bind=engine)
    
    # Create a database session
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_users = db.query(models.User).count()
        if existing_users > 0:
            print("Database already contains data. Skipping seed operation.")
            return
        
        print("Seeding database with initial data...")
        
        # Create levels with XP thresholds scaling up to 1 million
        levels = [
            {
                "level_number": 1,
                "title": "Foundations of Investing",
                "description": "Learn the basic concepts and terminology of investing.",
                "required_points": 0,
                "is_locked": False
            },
            {
                "level_number": 2,
                "title": "Trading Psychology & Emotional Discipline",
                "description": "Understand the psychological aspects of trading and develop emotional discipline.",
                "required_points": 1000,
                "is_locked": True
            },
            {
                "level_number": 3,
                "title": "Technical Analysis Essentials",
                "description": "Learn the basics of technical analysis and chart reading.",
                "required_points": 5000,
                "is_locked": True
            },
            {
                "level_number": 4,
                "title": "Fundamental Analysis & Valuation",
                "description": "Understand how to analyze company financials and value stocks.",
                "required_points": 10000,
                "is_locked": True
            },
            {
                "level_number": 5,
                "title": "Portfolio Construction & Asset Allocation",
                "description": "Learn how to build and manage a diversified investment portfolio.",
                "required_points": 20000,
                "is_locked": True
            },
            {
                "level_number": 6,
                "title": "Risk Management Strategies",
                "description": "Master techniques to manage and mitigate investment risks.",
                "required_points": 40000,
                "is_locked": True
            },
            {
                "level_number": 7,
                "title": "Advanced Trading Instruments",
                "description": "Explore options, futures, and other complex financial instruments.",
                "required_points": 80000,
                "is_locked": True
            },
            {
                "level_number": 8,
                "title": "Trading Styles & Market Approaches",
                "description": "Compare different trading styles and market approaches.",
                "required_points": 150000,
                "is_locked": True
            },
            {
                "level_number": 9,
                "title": "Macroeconomic Factors & Market Cycles",
                "description": "Understand how economic factors and market cycles affect investments.",
                "required_points": 400000,
                "is_locked": True
            },
            {
                "level_number": 10,
                "title": "Putting It All Together",
                "description": "Integrate all concepts into a comprehensive trading and investing strategy.",
                "required_points": 1000000,
                "is_locked": True
            }
        ]
        
        # Add levels to the database
        for level_data in levels:
            level = models.Level(**level_data)
            db.add(level)
        
        db.commit()
        
        # Create chapters for each level
        for level_number in range(1, 11):
            level = db.query(models.Level).filter(models.Level.level_number == level_number).first()
            
            # Create a chapter for this level
            chapter_data = {
                "title": f"Chapter {level_number}: {level.title}",
                "content": f"This is the content for Chapter {level_number}.",
                "order": 1,
                "level_id": level.id
            }
            
            chapter = models.Chapter(**chapter_data)
            db.add(chapter)
        
        db.commit()
        
        # Create quizzes for each chapter
        chapters = db.query(models.Chapter).all()
        for chapter in chapters:
            # Create a quiz for this chapter
            quiz_data = {
                "title": f"{chapter.title.split(':')[1].strip()} Quiz",
                "description": f"Test your knowledge of {chapter.title.split(':')[1].strip()}.",
                "points_reward": 100,
                "quiz_type": "regular",
                "chapter_id": chapter.id
            }
            
            quiz = models.Quiz(**quiz_data)
            db.add(quiz)
        
        db.commit()
        
        # Create questions for the first quiz (Level 1, Chapter 1)
        level1 = db.query(models.Level).filter(models.Level.level_number == 1).first()
        chapter1 = db.query(models.Chapter).filter(models.Chapter.level_id == level1.id).first()
        quiz1 = db.query(models.Quiz).filter(models.Quiz.chapter_id == chapter1.id).first()
        
        questions = [
            {
                "question_text": "What is the primary goal of investing?",
                "explanation": "The primary goal of investing is to grow wealth over time by putting money into assets that are expected to increase in value or generate income.",
                "options": [
                    {"option_text": "To make quick profits", "is_correct": False},
                    {"option_text": "To grow wealth over time", "is_correct": True},
                    {"option_text": "To avoid taxes", "is_correct": False},
                    {"option_text": "To beat inflation", "is_correct": False}
                ]
            },
            {
                "question_text": "Which of the following is considered the safest investment?",
                "explanation": "Government bonds, especially those issued by stable governments like the U.S., are generally considered the safest investments because they have the full backing of the government.",
                "options": [
                    {"option_text": "Stocks", "is_correct": False},
                    {"option_text": "Real estate", "is_correct": False},
                    {"option_text": "Government bonds", "is_correct": True},
                    {"option_text": "Cryptocurrencies", "is_correct": False}
                ]
            },
            {
                "question_text": "What is diversification?",
                "explanation": "Diversification is the strategy of spreading investments across various asset classes to reduce risk. It helps protect against significant losses if one investment performs poorly.",
                "options": [
                    {"option_text": "Investing all your money in one promising stock", "is_correct": False},
                    {"option_text": "Spreading investments across various asset classes to reduce risk", "is_correct": True},
                    {"option_text": "Investing only in foreign markets", "is_correct": False},
                    {"option_text": "Frequently buying and selling stocks", "is_correct": False}
                ]
            },
            {
                "question_text": "What is compound interest?",
                "explanation": "Compound interest is interest calculated on the initial principal and also on the accumulated interest over previous periods. It's often described as 'interest on interest.'",
                "options": [
                    {"option_text": "Interest that is paid only once", "is_correct": False},
                    {"option_text": "Interest calculated only on the principal amount", "is_correct": False},
                    {"option_text": "Interest calculated on both principal and accumulated interest", "is_correct": True},
                    {"option_text": "Interest that decreases over time", "is_correct": False}
                ]
            },
            {
                "question_text": "Which of the following is NOT a common asset class?",
                "explanation": "While stocks, bonds, and real estate are all common asset classes, warranties are not an asset class. Warranties are guarantees or promises made by manufacturers or sellers about their products.",
                "options": [
                    {"option_text": "Stocks", "is_correct": False},
                    {"option_text": "Bonds", "is_correct": False},
                    {"option_text": "Real estate", "is_correct": False},
                    {"option_text": "Warranties", "is_correct": True}
                ]
            }
        ]
        
        for question_data in questions:
            options_data = question_data.pop("options")
            
            question = models.Question(
                question_text=question_data["question_text"],
                explanation=question_data["explanation"],
                quiz_id=quiz1.id
            )
            db.add(question)
            db.commit()
            
            for option_data in options_data:
                option = models.QuestionOption(
                    option_text=option_data["option_text"],
                    is_correct=option_data["is_correct"],
                    question_id=question.id
                )
                db.add(option)
        
        db.commit()
        
        # Create a test user
        test_user = schemas.UserCreate(
            email="test@example.com",
            username="testuser",
            password="password123"
        )
        crud.create_user(db, test_user)
        
        # Create achievements for level completion
        achievements = [
            {
                "title": "Foundations Master",
                "description": "Complete all subsections in Chapter 1 and score at least 80% on the chapter quiz",
                "badge_image": "badge-foundations-master.png",
                "requirement_type": "quiz_score",
                "requirement_value": 80,
                "chapter_id": 1
            },
            {
                "title": "Psychology Expert",
                "description": "Complete all subsections in Chapter 2 and score at least 80% on the chapter quiz",
                "badge_image": "badge-psychology-expert.png",
                "requirement_type": "quiz_score",
                "requirement_value": 80,
                "chapter_id": 2
            },
            {
                "title": "Emotional Mastery",
                "description": "Complete the emotional self-assessment exercises in all subsections",
                "badge_image": "badge-emotional-mastery.png",
                "requirement_type": "subsection_completion",
                "requirement_value": 22,
                "chapter_id": 2
            },
            {
                "title": "Bias Buster",
                "description": "Correctly identify all cognitive biases in the Chapter 2 quiz",
                "badge_image": "badge-bias-buster.png",
                "requirement_type": "special_quiz_achievement",
                "requirement_value": 1,
                "chapter_id": 2
            },
            {
                "title": "Technical Analyst",
                "description": "Complete all chapters in Level 3",
                "badge_image": "badge-technical-analyst.png",
                "requirement_type": "level_completion",
                "requirement_value": 3,
                "chapter_id": None
            },
            {
                "title": "Fundamental Analyst",
                "description": "Complete all chapters in Level 4",
                "badge_image": "badge-fundamental-analyst.png",
                "requirement_type": "level_completion",
                "requirement_value": 4,
                "chapter_id": None
            },
            {
                "title": "Portfolio Manager",
                "description": "Complete all chapters in Level 5",
                "badge_image": "badge-portfolio-manager.png",
                "requirement_type": "level_completion",
                "requirement_value": 5,
                "chapter_id": None
            },
            {
                "title": "Risk Manager",
                "description": "Complete all chapters in Level 6",
                "badge_image": "badge-risk-manager.png",
                "requirement_type": "level_completion",
                "requirement_value": 6,
                "chapter_id": None
            },
            {
                "title": "Advanced Trader",
                "description": "Complete all chapters in Level 7",
                "badge_image": "badge-advanced-trader.png",
                "requirement_type": "level_completion",
                "requirement_value": 7,
                "chapter_id": None
            },
            {
                "title": "Trading Strategist",
                "description": "Complete all chapters in Level 8",
                "badge_image": "badge-trading-strategist.png",
                "requirement_type": "level_completion",
                "requirement_value": 8,
                "chapter_id": None
            },
            {
                "title": "Market Economist",
                "description": "Complete all chapters in Level 9",
                "badge_image": "badge-market-economist.png",
                "requirement_type": "level_completion",
                "requirement_value": 9,
                "chapter_id": None
            },
            {
                "title": "Master Investor",
                "description": "Complete all chapters in Level 10",
                "badge_image": "badge-master-investor.png",
                "requirement_type": "level_completion",
                "requirement_value": 10,
                "chapter_id": None
            }
        ]
        
        # Add achievements to the database
        for achievement_data in achievements:
            achievement = models.Achievement(**achievement_data)
            db.add(achievement)
        
        # Make sure to commit the achievements
        db.commit()
        
        # Add some general achievements
        general_achievements = [
            {
                "title": "First Steps",
                "description": "Complete your first quiz",
                "badge_image": "badge-first-steps.png",
                "requirement_type": "quiz_complete",
                "requirement_value": 1,
                "chapter_id": None
            },
            {
                "title": "Perfect Score",
                "description": "Get a perfect score on any quiz",
                "badge_image": "badge-perfect-score.png",
                "requirement_type": "quiz_score",
                "requirement_value": 100,
                "chapter_id": None
            },
            {
                "title": "Point Collector",
                "description": "Earn 100 points",
                "badge_image": "badge-point-collector.png",
                "requirement_type": "points_earned",
                "requirement_value": 100,
                "chapter_id": None
            },
            {
                "title": "Boss Slayer",
                "description": "Successfully complete a Boss Fight quiz",
                "badge_image": "badge-boss-slayer.png",
                "requirement_type": "boss_fight_complete",
                "requirement_value": 1,
                "chapter_id": None
            }
        ]
        
        # Add general achievements to the database
        for achievement_data in general_achievements:
            achievement = models.Achievement(**achievement_data)
            db.add(achievement)
        
        # Make sure to commit the general achievements
        db.commit()
        
        print("Database seeded successfully!")
    
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
