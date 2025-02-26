from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import psycopg

from . import models, schemas, crud, auth
from .db import engine, get_db
from .security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta
from .seed_data import seed_data

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Seed the database with initial data
seed_data()

app = FastAPI(title="Trading & Investing Gamified eBook API")

# Configure CORS for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://trading-learning-app-yfnvf7wl.devinapps.com"],  # Only allow the frontend domain
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Specify allowed methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

# Authentication endpoints
@app.post("/api/auth/register", response_model=schemas.UserWithGameData)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user with this email already exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Check if username is taken
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )
    
    # Create new user
    return crud.create_user(db=db, user=user)


@app.post("/api/auth/login", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Authenticate user
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/auth/me", response_model=schemas.UserWithGameData)
def read_users_me(
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return current_user


@app.get("/api/auth/onboarding", response_model=dict)
def get_onboarding_tutorial(
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Returns the onboarding tutorial content for new users.
    This is shown after successful registration.
    """
    return {
        "title": "Welcome to the Trading & Investing eBook!",
        "steps": [
            {
                "title": "Learn at Your Own Pace",
                "content": "Our interactive eBook allows you to learn about trading and investing at your own pace. Complete chapters, take quizzes, and earn points as you progress."
            },
            {
                "title": "Track Your Progress",
                "content": "Your dashboard shows your current level, points earned, and achievements. As you complete quizzes and challenges, you'll earn points and unlock new content."
            },
            {
                "title": "Earn Achievements",
                "content": "Collect badges and achievements as you master different aspects of trading and investing. Perfect scores, completing levels, and reaching point milestones all earn special recognition."
            },
            {
                "title": "Start Your Journey",
                "content": "Begin with Level 1: Foundations of Investing to learn the basics. Each level builds on the previous one, so make sure to master the fundamentals before moving on."
            }
        ],
        "is_new_user": current_user.created_at > (datetime.now() - timedelta(minutes=5))
    }


# User progress endpoints
@app.get("/api/users/progress", response_model=list[schemas.UserProgress])
def get_user_progress(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    return crud.get_user_progress_all(db, user_id=current_user.id)


@app.put("/api/users/progress/{level_id}", response_model=schemas.UserProgress)
def update_user_progress(
    level_id: int,
    progress: schemas.UserProgressUpdate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify level exists
    level = crud.get_level(db, level_id=level_id)
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")
    
    # Update progress
    return crud.create_or_update_user_progress(
        db=db,
        progress=progress,
        user_id=current_user.id
    )


@app.get("/api/users/achievements", response_model=list[schemas.UserAchievement])
def get_user_achievements(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    return crud.get_user_achievements(db, user_id=current_user.id)


@app.get("/api/users/quiz-attempts", response_model=list[schemas.QuizAttempt])
def get_user_quiz_attempts(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db),
    quiz_id: int = None
):
    return crud.get_quiz_attempts(db, user_id=current_user.id, quiz_id=quiz_id)


# Content endpoints
@app.get("/api/levels", response_model=list[schemas.Level])
def get_levels(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    levels = crud.get_levels(db)
    
    # Update locked status based on user's level
    for level in levels:
        if level.level_number <= current_user.current_level:
            level.is_locked = False
    
    return levels


@app.get("/api/levels/{level_id}", response_model=schemas.LevelWithChapters)
def get_level(
    level_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    level = crud.get_level(db, level_id=level_id)
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")
    
    # Check if user has access to this level
    if level.level_number > current_user.current_level:
        raise HTTPException(status_code=403, detail="Level locked")
    
    return level


@app.get("/api/chapters/{chapter_id}", response_model=schemas.ChapterWithQuizzes)
def get_chapter(
    chapter_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    chapter = crud.get_chapter(db, chapter_id=chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    # Check if user has access to this chapter's level
    level = crud.get_level(db, level_id=chapter.level_id)
    if level.level_number > current_user.current_level:
        raise HTTPException(status_code=403, detail="Chapter locked")
    
    return chapter


@app.get("/api/quizzes/{quiz_id}", response_model=schemas.QuizWithQuestions)
def get_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    quiz = crud.get_quiz(db, quiz_id=quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Check if user has access to this quiz's chapter's level
    chapter = crud.get_chapter(db, chapter_id=quiz.chapter_id)
    level = crud.get_level(db, level_id=chapter.level_id)
    if level.level_number > current_user.current_level:
        raise HTTPException(status_code=403, detail="Quiz locked")
    
    return quiz


@app.post("/api/quizzes/{quiz_id}/submit", response_model=schemas.QuizResult)
def submit_quiz(
    quiz_id: int,
    submission: schemas.QuizSubmission,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    # Check if quiz exists
    quiz = crud.get_quiz(db, quiz_id=quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Process submission
    result = crud.process_quiz_submission(
        db=db,
        user_id=current_user.id,
        quiz_id=quiz_id,
        answers=submission.answers
    )
    
    if not result:
        raise HTTPException(status_code=400, detail="Failed to process quiz submission")
    
    return result


# Gamification endpoints
@app.get("/api/leaderboard", response_model=list[schemas.LeaderboardEntry])
def get_leaderboard(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return crud.get_leaderboard(db, limit=limit)


@app.get("/api/achievements", response_model=list[schemas.Achievement])
def get_achievements(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    # Get all achievements
    achievements = crud.get_achievements(db)
    
    # Get user's earned achievements
    user_achievement_ids = [
        ua.achievement_id for ua in crud.get_user_achievements(db, user_id=current_user.id)
    ]
    
    # Mark achievements as earned
    for achievement in achievements:
        achievement.earned = achievement.id in user_achievement_ids
    
    return achievements


# Admin endpoints (protected)
# In a real application, we would add admin role checks here
@app.post("/api/admin/levels", response_model=schemas.Level)
def create_level(
    level: schemas.LevelCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return crud.create_level(db=db, level=level)


@app.post("/api/admin/chapters", response_model=schemas.Chapter)
def create_chapter(
    chapter: schemas.ChapterCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return crud.create_chapter(db=db, chapter=chapter)


@app.post("/api/admin/quizzes", response_model=schemas.Quiz)
def create_quiz(
    quiz: schemas.QuizCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return crud.create_quiz(db=db, quiz=quiz)


@app.post("/api/admin/questions", response_model=schemas.Question)
def create_question(
    question: schemas.QuestionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return crud.create_question(db=db, question=question)


@app.post("/api/admin/achievements", response_model=schemas.Achievement)
def create_achievement(
    achievement: schemas.AchievementCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return crud.create_achievement(db=db, achievement=achievement)
