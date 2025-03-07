from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import models, schemas, crud
import re

def import_chapter3_quiz():
    """
    Import the Chapter 3 quiz questions from the markdown file into the database.
    """
    # Create a database session
    db = SessionLocal()
    
    try:
        print("Starting Chapter 3 quiz import...")
        
        # Get Chapter 3
        chapter = db.query(models.Chapter).filter(models.Chapter.title.like("%Chapter 3:%")).first()
        
        if not chapter:
            print("Error: Chapter 3 not found. Make sure the database is seeded.")
            return False
        
        print(f"Found Chapter: {chapter.title}")
        
        # Check if quiz already exists
        existing_quiz = db.query(models.Quiz).filter(
            models.Quiz.title == "Technical Analysis Essentials Quiz",
            models.Quiz.chapter_id == chapter.id
        ).first()
        
        if existing_quiz:
            print(f"Quiz already exists: {existing_quiz.title}")
            quiz = existing_quiz
        else:
            # Create the quiz
            quiz_data = schemas.QuizCreate(
                title="Technical Analysis Essentials Quiz",
                description="Comprehensive quiz covering all aspects of technical analysis.",
                points_reward=1000,
                quiz_type="regular",
                chapter_id=chapter.id
            )
            quiz = crud.create_quiz(db, quiz_data)
            print(f"Created quiz: {quiz.title}")
        
        # Read the quiz questions from the markdown file
        with open("app/content/chapter3/chapter_quiz.md", "r") as f:
            content = f.read()
        
        # Extract questions and answers using regex
        question_pattern = r"### Question (\d+): .+?\n(.+?)\n- A\) (.+?)\n- B\) (.+?)\n- C\) (.+?)\n- D\) (.+?)\n"
        questions = re.findall(question_pattern, content, re.DOTALL)
        
        # Extract answer key
        answer_key_pattern = r"## Answer Key\n([\s\S]+?)\n\n"
        answer_key_match = re.search(answer_key_pattern, content)
        
        if not answer_key_match:
            print("Error: Answer key not found in markdown file.")
            return False
        
        answer_key_text = answer_key_match.group(1)
        answer_key = {}
        
        for line in answer_key_text.split("\n"):
            if line.strip():
                q_num, answer = line.split(".")
                answer_key[int(q_num)] = answer.strip()
        
        print(f"Found {len(questions)} questions and answer key.")
        
        # Add questions to the database
        for q_data in questions:
            q_num = int(q_data[0])
            q_text = q_data[1].strip()
            options = [q_data[2], q_data[3], q_data[4], q_data[5]]
            
            # Get the correct answer
            correct_answer = answer_key.get(q_num)
            if not correct_answer:
                print(f"Warning: No answer found for question {q_num}. Skipping.")
                continue
            
            # Map answer letter to index
            answer_map = {"A": 0, "B": 1, "C": 2, "D": 3}
            correct_index = answer_map.get(correct_answer)
            
            if correct_index is None:
                print(f"Warning: Invalid answer '{correct_answer}' for question {q_num}. Skipping.")
                continue
            
            # Create question options
            question_options = []
            for i, option_text in enumerate(options):
                option_data = schemas.QuestionOptionCreate(
                    option_text=option_text,
                    is_correct=i == correct_index
                )
                question_options.append(option_data)
            
            # Check if question already exists
            existing_question = db.query(models.Question).filter(
                models.Question.question_text == q_text,
                models.Question.quiz_id == quiz.id
            ).first()
            
            if existing_question:
                print(f"Question {q_num} already exists. Skipping.")
            else:
                # Create the question directly
                db_question = models.Question(
                    question_text=q_text,
                    explanation=f"This question tests understanding of technical analysis concepts.",
                    quiz_id=quiz.id
                )
                db.add(db_question)
                db.flush()  # Flush to get the question ID
                
                # Create the options directly
                for i, option_text in enumerate(options):
                    db_option = models.QuestionOption(
                        option_text=option_text,
                        is_correct=(i == correct_index),
                        question_id=db_question.id
                    )
                    db.add(db_option)
                
                db.commit()
                print(f"Added question {q_num}: {q_text[:50]}...")
        
        print("Chapter 3 quiz import completed successfully!")
        return True
    
    finally:
        db.close()

if __name__ == "__main__":
    import_chapter3_quiz()
