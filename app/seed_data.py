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
        level1 = schemas.LevelCreate(
            level_number=1,
            title="Foundations of Investing",
            description="Learn the basic terminology and concepts of investing",
            required_points=0,
            is_locked=False
        )
        db_level1 = crud.create_level(db, level1)
        
        level2 = schemas.LevelCreate(
            level_number=2,
            title="Trading Psychology",
            description="Understand the psychological aspects of trading and investing",
            required_points=100,
            is_locked=True
        )
        db_level2 = crud.create_level(db, level2)
        
        level3 = schemas.LevelCreate(
            level_number=3,
            title="Technical Analysis Basics",
            description="Learn how to read charts and identify patterns",
            required_points=250,
            is_locked=True
        )
        db_level3 = crud.create_level(db, level3)
        
        # Create chapters for Level 1
        chapter1 = schemas.ChapterCreate(
            title="Introduction to Investing",
            content="""
# Introduction to Investing

Investing is the act of allocating resources, usually money, with the expectation of generating an income or profit. 
You can invest in many different types of assets, including:

- Stocks
- Bonds
- Mutual Funds
- ETFs (Exchange-Traded Funds)
- Real Estate
- Commodities

## Why Invest?

Investing allows your money to work for you. When you invest, you're putting your money to work in a way that has the potential to grow in value over time.

## Key Investment Concepts

1. **Risk vs. Return**: Generally, the higher the potential return, the higher the risk.
2. **Diversification**: Spreading investments across different asset types to reduce risk.
3. **Compound Interest**: Earning interest on both the initial principal and accumulated interest.
4. **Time Horizon**: The length of time you plan to hold an investment before needing the money.

In the following chapters, we'll explore these concepts in more detail and learn about different investment vehicles.
            """,
            order=1,
            level_id=db_level1.id
        )
        db_chapter1 = crud.create_chapter(db, chapter1)
        
        chapter2 = schemas.ChapterCreate(
            title="Understanding Stocks",
            content="""
# Understanding Stocks

A stock represents ownership in a company. When you buy a stock, you're purchasing a small piece of that company, which makes you a shareholder.

## Stock Basics

- **Shares**: Units of ownership in a company.
- **Market Capitalization**: The total value of a company's outstanding shares.
- **Dividends**: Payments made by a company to its shareholders.
- **Stock Exchange**: A marketplace where stocks are bought and sold.

## Types of Stocks

1. **Common Stocks**: Represent ownership in a company and may provide voting rights.
2. **Preferred Stocks**: Usually don't have voting rights but have priority over common stocks for dividend payments.
3. **Growth Stocks**: Companies expected to grow at an above-average rate.
4. **Value Stocks**: Companies that appear to be undervalued based on their fundamentals.
5. **Dividend Stocks**: Companies that pay regular dividends to shareholders.

## How to Evaluate Stocks

- **Price-to-Earnings (P/E) Ratio**: Compares a company's share price to its earnings per share.
- **Earnings Per Share (EPS)**: A company's profit divided by its outstanding shares.
- **Price-to-Book (P/B) Ratio**: Compares a company's market value to its book value.
- **Dividend Yield**: Annual dividends per share divided by price per share.

Understanding these concepts will help you make more informed investment decisions when it comes to stocks.
            """,
            order=2,
            level_id=db_level1.id
        )
        db_chapter2 = crud.create_chapter(db, chapter2)
        
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
        
        # Create achievements
        achievement1 = schemas.AchievementCreate(
            title="First Steps",
            description="Complete your first quiz",
            badge_image="badge_first_steps.png",
            requirement_type="quiz_complete",
            requirement_value=1
        )
        crud.create_achievement(db, achievement1)
        
        achievement2 = schemas.AchievementCreate(
            title="Perfect Score",
            description="Get a perfect score on any quiz",
            badge_image="badge_perfect_score.png",
            requirement_type="quiz_score",
            requirement_value=100
        )
        crud.create_achievement(db, achievement2)
        
        achievement3 = schemas.AchievementCreate(
            title="Level 1 Master",
            description="Complete Level 1",
            badge_image="badge_level1_master.png",
            requirement_type="level_complete",
            requirement_value=1
        )
        crud.create_achievement(db, achievement3)
        
        achievement4 = schemas.AchievementCreate(
            title="Point Collector",
            description="Earn 100 points",
            badge_image="badge_point_collector.png",
            requirement_type="points_earned",
            requirement_value=100
        )
        crud.create_achievement(db, achievement4)
        
        achievement5 = schemas.AchievementCreate(
            title="Boss Slayer",
            description="Successfully complete a Boss Fight quiz",
            badge_image="badge_boss_slayer.png",
            requirement_type="boss_fight_complete",
            requirement_value=1
        )
        crud.create_achievement(db, achievement5)
        
        print("Database seeded successfully!")
    
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
