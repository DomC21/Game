"""
Seed script to populate the database with initial data for testing.
"""
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .db import SessionLocal, engine

# Create tables
models.Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(models.Level).count() > 0:
            print("Database already contains data. Skipping seed.")
            return
        
        # Create levels
        levels = [
            {
                "level_number": 1,
                "title": "Foundations of Investing",
                "description": "Learn the basic terminology, asset types, and fundamental concepts",
                "required_points": 0,
                "is_locked": False
            },
            {
                "level_number": 2,
                "title": "Trading Psychology & Emotional Discipline",
                "description": "Master emotional discipline, risk appetite, and trading mindset",
                "required_points": 1000,
                "is_locked": True
            },
            {
                "level_number": 3,
                "title": "Technical Analysis Essentials",
                "description": "Learn chart reading, support/resistance, and trend lines",
                "required_points": 5000,
                "is_locked": True
            },
            {
                "level_number": 4,
                "title": "Fundamental Analysis & Valuation",
                "description": "Understand financial statements, ratios, and company valuation",
                "required_points": 10000,
                "is_locked": True
            },
            {
                "level_number": 5,
                "title": "Portfolio Construction & Asset Allocation",
                "description": "Learn to build diversified portfolios and allocate assets effectively",
                "required_points": 20000,
                "is_locked": True
            },
            {
                "level_number": 6,
                "title": "Risk Management Strategies",
                "description": "Master techniques to protect your investments and manage risk",
                "required_points": 40000,
                "is_locked": True
            },
            {
                "level_number": 7,
                "title": "Advanced Trading Instruments",
                "description": "Explore options, futures, and other complex financial instruments",
                "required_points": 80000,
                "is_locked": True
            },
            {
                "level_number": 8,
                "title": "Trading Styles & Market Approaches",
                "description": "Compare swing, day, and long-term trading strategies",
                "required_points": 150000,
                "is_locked": True
            },
            {
                "level_number": 9,
                "title": "Macroeconomic Factors & Market Cycles",
                "description": "Understand how economic factors influence markets",
                "required_points": 400000,
                "is_locked": True
            },
            {
                "level_number": 10,
                "title": "Putting It All Together & Continuous Improvement",
                "description": "Integrate all concepts and develop a personal trading plan",
                "required_points": 1000000,
                "is_locked": True
            }
        ]
        
        # Add levels to the database
        level_objects = []
        for level_data in levels:
            level = models.Level(**level_data)
            db.add(level)
            db.flush()
            level_objects.append(level)
        
        # Store references to the first three levels for backward compatibility with existing code
        db_level1 = level_objects[0]
        db_level2 = level_objects[1]
        db_level3 = level_objects[2]
        
        # Function to create placeholder chapters for a level
        def create_placeholder_chapters(db, level_id, level_number, base_title):
            chapters = []
            for i in range(1, 21):  # Create 20 chapters per level
                chapter_title = f"{base_title} {i}"
                chapter_content = f"""
# {chapter_title}

## Subsection 1: Introduction
This is an introduction to {chapter_title}.

## Subsection 2: Key Concepts
These are the key concepts for {chapter_title}.

## Subsection 3: Examples
Here are some examples for {chapter_title}.

## Subsection 4: Practice
Practice exercises for {chapter_title}.

## Subsection 5: Summary
Summary of {chapter_title}.
"""
                
                chapter = models.Chapter(
                    title=chapter_title,
                    content=chapter_content,
                    order=i,
                    level_id=level_id
                )
                db.add(chapter)
                db.flush()
                chapters.append(chapter)
                
                # Create a quiz for each chapter
                quiz = models.Quiz(
                    title=f"Quiz: {chapter_title}",
                    description=f"Test your knowledge of {chapter_title}",
                    points_reward=10,
                    quiz_type="regular",
                    chapter_id=chapter.id
                )
                db.add(quiz)
                db.flush()
                
                # Create placeholder questions for the quiz
                for j in range(1, 6):  # 5 questions per quiz
                    question = models.Question(
                        question_text=f"Question {j} for {chapter_title}?",
                        explanation=f"Explanation for question {j}",
                        quiz_id=quiz.id
                    )
                    db.add(question)
                    db.flush()
                    
                    # Create options for the question
                    for k in range(1, 5):  # 4 options per question
                        option = models.QuestionOption(
                            option_text=f"Option {k} for question {j}",
                            is_correct=(k == 1),  # First option is correct
                            question_id=question.id
                        )
                        db.add(option)
            
            return chapters
        
        # Create chapters for each level
        all_chapters = []
        for level in level_objects:
            level_chapters = create_placeholder_chapters(db, level.id, level.level_number, level.title)
            all_chapters.extend(level_chapters)
        
        # Store references to the first two chapters for backward compatibility with existing code
        db_chapter1 = all_chapters[0]
        db_chapter2 = all_chapters[1]
        
        # Create quiz for Chapter 1
        quiz1 = schemas.QuizCreate(
            title="Introduction to Investing Quiz",
            description="Test your knowledge of basic investing concepts",
            points_reward=50,
            quiz_type="regular",
            chapter_id=db_chapter1.id
        )
        db_quiz1 = crud.create_quiz(db, quiz1)
        
        # Create "Boss Fight" quiz for Chapter 2
        quiz2 = schemas.QuizCreate(
            title="Stock Market Boss Challenge",
            description="Test your mastery of stock market concepts",
            points_reward=100,
            quiz_type="boss_fight",
            chapter_id=db_chapter2.id
        )
        db_quiz2 = crud.create_quiz(db, quiz2)
        
        # Create questions for Quiz 1
        # First, create the question without options
        question1 = models.Question(
            question_text="What is investing?",
            explanation="Investing is allocating resources with the expectation of generating income or profit.",
            quiz_id=db_quiz1.id
        )
        db.add(question1)
        db.commit()
        db.refresh(question1)
        
        # Then add options to the question
        option1_1 = models.QuestionOption(
            option_text="Spending money on consumer goods",
            is_correct=False,
            question_id=question1.id
        )
        option1_2 = models.QuestionOption(
            option_text="Allocating resources with the expectation of generating income or profit",
            is_correct=True,
            question_id=question1.id
        )
        option1_3 = models.QuestionOption(
            option_text="Saving money in a checking account",
            is_correct=False,
            question_id=question1.id
        )
        option1_4 = models.QuestionOption(
            option_text="Borrowing money from a bank",
            is_correct=False,
            question_id=question1.id
        )
        db.add_all([option1_1, option1_2, option1_3, option1_4])
        db.commit()
        
        # Create question 2
        question2 = models.Question(
            question_text="Which of the following is NOT a common investment asset?",
            explanation="Credit card debt is a liability, not an investment asset.",
            quiz_id=db_quiz1.id
        )
        db.add(question2)
        db.commit()
        db.refresh(question2)
        
        # Add options to question 2
        option2_1 = models.QuestionOption(
            option_text="Stocks",
            is_correct=False,
            question_id=question2.id
        )
        option2_2 = models.QuestionOption(
            option_text="Bonds",
            is_correct=False,
            question_id=question2.id
        )
        option2_3 = models.QuestionOption(
            option_text="Real Estate",
            is_correct=False,
            question_id=question2.id
        )
        option2_4 = models.QuestionOption(
            option_text="Credit Card Debt",
            is_correct=True,
            question_id=question2.id
        )
        db.add_all([option2_1, option2_2, option2_3, option2_4])
        db.commit()
        
        # Create question 3
        question3 = models.Question(
            question_text="What is compound interest?",
            explanation="Compound interest is when you earn interest on both the initial principal and the accumulated interest.",
            quiz_id=db_quiz1.id
        )
        db.add(question3)
        db.commit()
        db.refresh(question3)
        
        # Add options to question 3
        option3_1 = models.QuestionOption(
            option_text="Interest that only applies to the initial investment",
            is_correct=False,
            question_id=question3.id
        )
        option3_2 = models.QuestionOption(
            option_text="Interest earned on both the initial principal and accumulated interest",
            is_correct=True,
            question_id=question3.id
        )
        option3_3 = models.QuestionOption(
            option_text="A fixed interest rate that never changes",
            is_correct=False,
            question_id=question3.id
        )
        option3_4 = models.QuestionOption(
            option_text="Interest paid to the government as tax",
            is_correct=False,
            question_id=question3.id
        )
        db.add_all([option3_1, option3_2, option3_3, option3_4])
        db.commit()
        
        # Create questions for the Boss Fight Quiz (Quiz 2)
        # Question 1
        boss_q1 = models.Question(
            question_text="What is the P/E ratio used for?",
            explanation="The Price-to-Earnings (P/E) ratio is used to evaluate a company's valuation relative to its earnings.",
            quiz_id=db_quiz2.id
        )
        db.add(boss_q1)
        db.commit()
        db.refresh(boss_q1)
        
        # Add options to boss question 1
        boss_q1_opt1 = models.QuestionOption(
            option_text="To measure a company's debt level",
            is_correct=False,
            question_id=boss_q1.id
        )
        boss_q1_opt2 = models.QuestionOption(
            option_text="To evaluate a company's valuation relative to its earnings",
            is_correct=True,
            question_id=boss_q1.id
        )
        boss_q1_opt3 = models.QuestionOption(
            option_text="To calculate dividend payments",
            is_correct=False,
            question_id=boss_q1.id
        )
        boss_q1_opt4 = models.QuestionOption(
            option_text="To determine a company's market share",
            is_correct=False,
            question_id=boss_q1.id
        )
        db.add_all([boss_q1_opt1, boss_q1_opt2, boss_q1_opt3, boss_q1_opt4])
        db.commit()
        
        # Question 2
        boss_q2 = models.Question(
            question_text="Which of the following is a characteristic of preferred stock?",
            explanation="Preferred stock typically has priority over common stock for dividend payments.",
            quiz_id=db_quiz2.id
        )
        db.add(boss_q2)
        db.commit()
        db.refresh(boss_q2)
        
        # Add options to boss question 2
        boss_q2_opt1 = models.QuestionOption(
            option_text="Always has voting rights",
            is_correct=False,
            question_id=boss_q2.id
        )
        boss_q2_opt2 = models.QuestionOption(
            option_text="Never pays dividends",
            is_correct=False,
            question_id=boss_q2.id
        )
        boss_q2_opt3 = models.QuestionOption(
            option_text="Priority over common stock for dividend payments",
            is_correct=True,
            question_id=boss_q2.id
        )
        boss_q2_opt4 = models.QuestionOption(
            option_text="Cannot be sold on stock exchanges",
            is_correct=False,
            question_id=boss_q2.id
        )
        db.add_all([boss_q2_opt1, boss_q2_opt2, boss_q2_opt3, boss_q2_opt4])
        db.commit()
        
        # Question 3
        boss_q3 = models.Question(
            question_text="What is market capitalization?",
            explanation="Market capitalization is the total value of a company's outstanding shares, calculated by multiplying the share price by the number of shares outstanding.",
            quiz_id=db_quiz2.id
        )
        db.add(boss_q3)
        db.commit()
        db.refresh(boss_q3)
        
        # Add options to boss question 3
        boss_q3_opt1 = models.QuestionOption(
            option_text="The total debt of a company",
            is_correct=False,
            question_id=boss_q3.id
        )
        boss_q3_opt2 = models.QuestionOption(
            option_text="The total value of a company's outstanding shares",
            is_correct=True,
            question_id=boss_q3.id
        )
        boss_q3_opt3 = models.QuestionOption(
            option_text="The total revenue of a company",
            is_correct=False,
            question_id=boss_q3.id
        )
        boss_q3_opt4 = models.QuestionOption(
            option_text="The total number of employees in a company",
            is_correct=False,
            question_id=boss_q3.id
        )
        db.add_all([boss_q3_opt1, boss_q3_opt2, boss_q3_opt3, boss_q3_opt4])
        db.commit()
        
        # Question 4
        boss_q4 = models.Question(
            question_text="What is a dividend yield?",
            explanation="Dividend yield is the annual dividend per share divided by the share price, expressed as a percentage.",
            quiz_id=db_quiz2.id
        )
        db.add(boss_q4)
        db.commit()
        db.refresh(boss_q4)
        
        # Add options to boss question 4
        boss_q4_opt1 = models.QuestionOption(
            option_text="The total amount of dividends paid by a company",
            is_correct=False,
            question_id=boss_q4.id
        )
        boss_q4_opt2 = models.QuestionOption(
            option_text="The growth rate of dividends over time",
            is_correct=False,
            question_id=boss_q4.id
        )
        boss_q4_opt3 = models.QuestionOption(
            option_text="Annual dividend per share divided by share price, expressed as a percentage",
            is_correct=True,
            question_id=boss_q4.id
        )
        boss_q4_opt4 = models.QuestionOption(
            option_text="The frequency of dividend payments",
            is_correct=False,
            question_id=boss_q4.id
        )
        db.add_all([boss_q4_opt1, boss_q4_opt2, boss_q4_opt3, boss_q4_opt4])
        db.commit()
        
        # Question 5
        boss_q5 = models.Question(
            question_text="Which of the following is a characteristic of growth stocks?",
            explanation="Growth stocks are shares in companies expected to grow at an above-average rate compared to other companies in the market.",
            quiz_id=db_quiz2.id
        )
        db.add(boss_q5)
        db.commit()
        db.refresh(boss_q5)
        
        # Add options to boss question 5
        boss_q5_opt1 = models.QuestionOption(
            option_text="Companies expected to grow at an above-average rate",
            is_correct=True,
            question_id=boss_q5.id
        )
        boss_q5_opt2 = models.QuestionOption(
            option_text="Companies that always pay high dividends",
            is_correct=False,
            question_id=boss_q5.id
        )
        boss_q5_opt3 = models.QuestionOption(
            option_text="Companies with low P/E ratios",
            is_correct=False,
            question_id=boss_q5.id
        )
        boss_q5_opt4 = models.QuestionOption(
            option_text="Companies that are undervalued based on fundamentals",
            is_correct=False,
            question_id=boss_q5.id
        )
        db.add_all([boss_q5_opt1, boss_q5_opt2, boss_q5_opt3, boss_q5_opt4])
        db.commit()
        
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
                "description": "Complete all chapters in Level 2",
                "badge_image": "badge-psychology-expert.png",
                "requirement_type": "level_completion",
                "requirement_value": 2
            },
            {
                "title": "Technical Analyst",
                "description": "Complete all chapters in Level 3",
                "badge_image": "badge-technical-analyst.png",
                "requirement_type": "level_completion",
                "requirement_value": 3
            },
            {
                "title": "Fundamental Analyst",
                "description": "Complete all chapters in Level 4",
                "badge_image": "badge-fundamental-analyst.png",
                "requirement_type": "level_completion",
                "requirement_value": 4
            },
            {
                "title": "Portfolio Manager",
                "description": "Complete all chapters in Level 5",
                "badge_image": "badge-portfolio-manager.png",
                "requirement_type": "level_completion",
                "requirement_value": 5
            },
            {
                "title": "Risk Manager",
                "description": "Complete all chapters in Level 6",
                "badge_image": "badge-risk-manager.png",
                "requirement_type": "level_completion",
                "requirement_value": 6
            },
            {
                "title": "Advanced Trader",
                "description": "Complete all chapters in Level 7",
                "badge_image": "badge-advanced-trader.png",
                "requirement_type": "level_completion",
                "requirement_value": 7
            },
            {
                "title": "Trading Strategist",
                "description": "Complete all chapters in Level 8",
                "badge_image": "badge-trading-strategist.png",
                "requirement_type": "level_completion",
                "requirement_value": 8
            },
            {
                "title": "Market Economist",
                "description": "Complete all chapters in Level 9",
                "badge_image": "badge-market-economist.png",
                "requirement_type": "level_completion",
                "requirement_value": 9
            },
            {
                "title": "Master Investor",
                "description": "Complete all chapters in Level 10",
                "badge_image": "badge-master-investor.png",
                "requirement_type": "level_completion",
                "requirement_value": 10
            }
        ]
        
        # Add achievements to the database
        for achievement_data in achievements:
            achievement = models.Achievement(**achievement_data)
            db.add(achievement)
        
        # Add some general achievements
        general_achievements = [
            {
                "title": "First Steps",
                "description": "Complete your first quiz",
                "badge_image": "badge-first-steps.png",
                "requirement_type": "quiz_complete",
                "requirement_value": 1
            },
            {
                "title": "Perfect Score",
                "description": "Get a perfect score on any quiz",
                "badge_image": "badge-perfect-score.png",
                "requirement_type": "quiz_score",
                "requirement_value": 100
            },
            {
                "title": "Point Collector",
                "description": "Earn 100 points",
                "badge_image": "badge-point-collector.png",
                "requirement_type": "points_earned",
                "requirement_value": 100
            },
            {
                "title": "Boss Slayer",
                "description": "Successfully complete a Boss Fight quiz",
                "badge_image": "badge-boss-slayer.png",
                "requirement_type": "boss_fight_complete",
                "requirement_value": 1
            }
        ]
        
        # Add general achievements to the database
        for achievement_data in general_achievements:
            achievement = models.Achievement(**achievement_data)
            db.add(achievement)
        
        print("Database seeded successfully!")
    
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
