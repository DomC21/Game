from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import List, Dict, Optional, Tuple

from . import models, schemas
from .security import get_password_hash, verify_password


# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        current_level=1,
        total_points=0,
        experience_points=0
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# Level CRUD operations
def get_level(db: Session, level_id: int):
    return db.query(models.Level).filter(models.Level.id == level_id).first()


def get_level_by_number(db: Session, level_number: int):
    return db.query(models.Level).filter(models.Level.level_number == level_number).first()


def get_levels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Level).order_by(models.Level.level_number).offset(skip).limit(limit).all()


def create_level(db: Session, level: schemas.LevelCreate):
    db_level = models.Level(**level.dict())
    db.add(db_level)
    db.commit()
    db.refresh(db_level)
    return db_level


# Chapter CRUD operations
def get_chapter(db: Session, chapter_id: int):
    return db.query(models.Chapter).filter(models.Chapter.id == chapter_id).first()


def get_chapters_by_level(db: Session, level_id: int):
    return db.query(models.Chapter).filter(models.Chapter.level_id == level_id).order_by(models.Chapter.order).all()


def create_chapter(db: Session, chapter: schemas.ChapterCreate):
    db_chapter = models.Chapter(**chapter.dict())
    db.add(db_chapter)
    db.commit()
    db.refresh(db_chapter)
    return db_chapter


# Quiz CRUD operations
def get_quiz(db: Session, quiz_id: int):
    return db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()


def get_quizzes_by_chapter(db: Session, chapter_id: int):
    return db.query(models.Quiz).filter(models.Quiz.chapter_id == chapter_id).all()


def create_quiz(db: Session, quiz: schemas.QuizCreate):
    db_quiz = models.Quiz(**quiz.dict())
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz


# Question CRUD operations
def get_question(db: Session, question_id: int):
    return db.query(models.Question).filter(models.Question.id == question_id).first()


def get_questions_by_quiz(db: Session, quiz_id: int):
    return db.query(models.Question).filter(models.Question.quiz_id == quiz_id).all()


def create_question(db: Session, question: schemas.QuestionCreate):
    # Extract options from the question data
    options_data = question.dict().pop("options")
    
    # Create the question
    db_question = models.Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    
    # Create options for the question
    for option_data in options_data:
        option_dict = option_data.dict() if hasattr(option_data, 'dict') else option_data
        db_option = models.QuestionOption(**option_dict, question_id=db_question.id)
        db.add(db_option)
    
    db.commit()
    db.refresh(db_question)
    return db_question


# Achievement CRUD operations
def get_achievement(db: Session, achievement_id: int):
    return db.query(models.Achievement).filter(models.Achievement.id == achievement_id).first()


def get_achievements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Achievement).offset(skip).limit(limit).all()


def create_achievement(db: Session, achievement: schemas.AchievementCreate):
    db_achievement = models.Achievement(**achievement.dict())
    db.add(db_achievement)
    db.commit()
    db.refresh(db_achievement)
    return db_achievement


# User Progress CRUD operations
def get_user_progress(db: Session, user_id: int, level_id: int):
    return db.query(models.UserProgress).filter(
        models.UserProgress.user_id == user_id,
        models.UserProgress.level_id == level_id
    ).first()


def get_user_progress_all(db: Session, user_id: int):
    return db.query(models.UserProgress).filter(models.UserProgress.user_id == user_id).all()


def create_or_update_user_progress(db: Session, progress: schemas.UserProgressUpdate, user_id: int):
    db_progress = get_user_progress(db, user_id, progress.level_id)
    
    if db_progress:
        db_progress.is_completed = progress.is_completed
        db_progress.last_accessed = datetime.now()
    else:
        db_progress = models.UserProgress(
            user_id=user_id,
            level_id=progress.level_id,
            is_completed=progress.is_completed
        )
        db.add(db_progress)
    
    db.commit()
    db.refresh(db_progress)
    return db_progress


# User Achievement CRUD operations
def get_user_achievement(db: Session, user_id: int, achievement_id: int):
    return db.query(models.UserAchievement).filter(
        models.UserAchievement.user_id == user_id,
        models.UserAchievement.achievement_id == achievement_id
    ).first()


def get_user_achievements(db: Session, user_id: int):
    return db.query(models.UserAchievement).filter(models.UserAchievement.user_id == user_id).all()


def award_achievement(db: Session, user_id: int, achievement_id: int):
    # Check if user already has this achievement
    existing = get_user_achievement(db, user_id, achievement_id)
    if existing:
        return existing
    
    # Create new user achievement
    db_user_achievement = models.UserAchievement(
        user_id=user_id,
        achievement_id=achievement_id
    )
    db.add(db_user_achievement)
    db.commit()
    db.refresh(db_user_achievement)
    return db_user_achievement


# Quiz Attempt CRUD operations
def create_quiz_attempt(db: Session, attempt: schemas.QuizAttemptCreate):
    db_attempt = models.QuizAttempt(**attempt.dict())
    db.add(db_attempt)
    db.commit()
    db.refresh(db_attempt)
    return db_attempt


def get_quiz_attempts(db: Session, user_id: int, quiz_id: Optional[int] = None):
    query = db.query(models.QuizAttempt).filter(models.QuizAttempt.user_id == user_id)
    
    if quiz_id:
        query = query.filter(models.QuizAttempt.quiz_id == quiz_id)
    
    return query.order_by(models.QuizAttempt.completed_at.desc()).all()


# Gamification functions
def add_points_to_user(db: Session, user_id: int, points: int) -> Tuple[models.User, bool, Optional[int]]:
    """
    Add points to a user and check if they level up.
    Returns: (updated_user, did_level_up, new_level_if_leveled_up)
    """
    user = get_user(db, user_id)
    if not user:
        return None, False, None
    
    # Add points
    user.total_points += points
    user.experience_points += points
    
    # Check for level up
    current_level = get_level_by_number(db, user.current_level)
    next_level = get_level_by_number(db, user.current_level + 1)
    
    level_up = False
    new_level = None
    
    if next_level and user.experience_points >= next_level.required_points:
        user.current_level += 1
        user.experience_points = user.experience_points - next_level.required_points
        level_up = True
        new_level = user.current_level
    
    db.commit()
    db.refresh(user)
    return user, level_up, new_level


def check_achievements(db: Session, user_id: int) -> List[models.Achievement]:
    """
    Check if user has earned any new achievements and award them.
    Returns a list of newly awarded achievements.
    """
    user = get_user(db, user_id)
    if not user:
        return []
    
    # Get all achievements
    all_achievements = get_achievements(db)
    
    # Get user's existing achievements
    user_achievement_ids = [ua.achievement_id for ua in get_user_achievements(db, user_id)]
    
    # Check each achievement to see if user qualifies
    new_achievements = []
    
    for achievement in all_achievements:
        # Skip if user already has this achievement
        if achievement.id in user_achievement_ids:
            continue
        
        earned = False
        
        # Check different achievement types
        if achievement.requirement_type == "points_earned":
            earned = user.total_points >= achievement.requirement_value
        
        elif achievement.requirement_type == "level_complete":
            # Check if user has completed the specified level
            level_progress = get_user_progress(db, user_id, achievement.requirement_value)
            earned = level_progress and level_progress.is_completed
        
        elif achievement.requirement_type == "quiz_score":
            # Check if user has achieved a perfect score on any quiz
            quiz_attempts = get_quiz_attempts(db, user_id)
            for attempt in quiz_attempts:
                if attempt.score == attempt.max_score:
                    earned = True
                    break
        
        elif achievement.requirement_type == "quiz_complete":
            # Check if user has completed at least the required number of quizzes
            quiz_attempts = get_quiz_attempts(db, user_id)
            earned = len(quiz_attempts) >= achievement.requirement_value
        
        elif achievement.requirement_type == "boss_fight_complete":
            # Check if user has completed a boss fight quiz
            quiz_attempts = get_quiz_attempts(db, user_id)
            for attempt in quiz_attempts:
                quiz = get_quiz(db, attempt.quiz_id)
                if quiz and quiz.quiz_type == "boss_fight" and attempt.score / attempt.max_score >= 0.8:
                    earned = True
                    break
        
        # Award achievement if earned
        if earned:
            award_achievement(db, user_id, achievement.id)
            new_achievements.append(achievement)
    
    return new_achievements


def process_quiz_submission(
    db: Session, 
    user_id: int, 
    quiz_id: int, 
    answers: Dict[int, int]
) -> schemas.QuizResult:
    """
    Process a quiz submission, calculate score, award points, and check for achievements.
    Returns a QuizResult object with the results.
    """
    # Get the quiz
    quiz = get_quiz(db, quiz_id)
    if not quiz:
        return None
    
    # Get all questions for this quiz
    questions = get_questions_by_quiz(db, quiz_id)
    
    # If there are no questions, return a default result
    if not questions:
        result = schemas.QuizResult(
            quiz_id=quiz_id,
            score=0,
            max_score=0,
            points_earned=0,
            correct_answers={},
            new_achievements=[],
            level_up=False,
            new_level=None
        )
        return result
    
    # Calculate score
    score = 0
    max_score = len(questions)
    correct_answers = {}
    
    for question in questions:
        # Get the selected option
        selected_option_id = answers.get(question.id)
        if not selected_option_id:
            correct_answers[question.id] = False
            continue
        
        # Check if the selected option is correct
        is_correct = False
        for option in question.options:
            if option.id == selected_option_id and option.is_correct:
                is_correct = True
                score += 1
                break
        
        correct_answers[question.id] = is_correct
    
    # Calculate points earned (based on percentage correct)
    # For boss fight quizzes, we require at least 80% correct to earn any points
    if quiz.quiz_type == "boss_fight":
        score_percentage = (score / max_score) if max_score > 0 else 0
        if score_percentage >= 0.8:  # 80% or higher
            # Bonus points for boss fights
            points_earned = int(quiz.points_reward * score_percentage * 1.5)  # 50% bonus
        else:
            points_earned = 0  # No points if below 80%
    else:
        # Regular quizzes award points proportionally
        points_earned = int(quiz.points_reward * (score / max_score)) if max_score > 0 else 0
    
    # Create quiz attempt record
    attempt = schemas.QuizAttemptCreate(
        user_id=user_id,
        quiz_id=quiz_id,
        score=score,
        max_score=max_score,
        points_earned=points_earned
    )
    create_quiz_attempt(db, attempt)
    
    # Add points to user and check for level up
    user, level_up, new_level = add_points_to_user(db, user_id, points_earned)
    
    # Check for new achievements
    new_achievements = check_achievements(db, user_id)
    
    # Create and return result
    # Convert Achievement model objects to dictionaries for Pydantic
    achievement_dicts = []
    for achievement in new_achievements:
        achievement_dict = {
            "id": achievement.id,
            "title": achievement.title,
            "description": achievement.description,
            "badge_image": achievement.badge_image,
            "requirement_type": achievement.requirement_type,
            "requirement_value": achievement.requirement_value,
            "earned": True
        }
        achievement_dicts.append(achievement_dict)
    
    result = schemas.QuizResult(
        quiz_id=quiz_id,
        score=score,
        max_score=max_score,
        points_earned=points_earned,
        correct_answers=correct_answers,
        new_achievements=achievement_dicts,
        level_up=level_up,
        new_level=new_level
    )
    
    return result


# Leaderboard functions
def get_leaderboard(db: Session, limit: int = 10) -> List[models.User]:
    """Get top users by total points."""
    return db.query(models.User).order_by(models.User.total_points.desc()).limit(limit).all()
