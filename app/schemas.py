from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None


class UserProgressUpdate(BaseModel):
    level_id: int
    is_completed: bool


# Level schemas
class LevelBase(BaseModel):
    level_number: int
    title: str
    description: str
    required_points: int
    is_locked: bool = True


class LevelCreate(LevelBase):
    pass


class Level(LevelBase):
    id: int

    class Config:
        orm_mode = True


class LevelWithChapters(Level):
    chapters: List["Chapter"] = []

    class Config:
        orm_mode = True


# Chapter schemas
class ChapterBase(BaseModel):
    title: str
    content: str
    order: int


class ChapterCreate(ChapterBase):
    level_id: int


class Chapter(ChapterBase):
    id: int
    level_id: int

    class Config:
        orm_mode = True


class ChapterWithQuizzes(Chapter):
    quizzes: List["Quiz"] = []

    class Config:
        orm_mode = True


# Quiz schemas
class QuizBase(BaseModel):
    title: str
    description: str
    points_reward: int = 10
    quiz_type: str = "regular"  # "regular", "boss_fight", "mini_challenge"


class QuizCreate(QuizBase):
    chapter_id: int


class Quiz(QuizBase):
    id: int
    chapter_id: int

    class Config:
        orm_mode = True


class QuizWithQuestions(Quiz):
    questions: List["QuestionWithOptions"] = []

    class Config:
        orm_mode = True


# Question option schemas
class QuestionOptionBase(BaseModel):
    option_text: str
    is_correct: bool = False


class QuestionOptionCreate(QuestionOptionBase):
    pass


class QuestionOption(QuestionOptionBase):
    id: int

    class Config:
        orm_mode = True


# Question schemas
class QuestionBase(BaseModel):
    question_text: str
    explanation: Optional[str] = None


class QuestionCreate(QuestionBase):
    quiz_id: int
    options: List[QuestionOptionCreate]


class Question(QuestionBase):
    id: int
    quiz_id: int

    class Config:
        orm_mode = True


class QuestionWithOptions(Question):
    options: List[QuestionOption] = []

    class Config:
        orm_mode = True


# Achievement schemas
class AchievementBase(BaseModel):
    title: str
    description: str
    badge_image: str
    requirement_type: str
    requirement_value: int
    chapter_id: Optional[int] = None


class AchievementCreate(AchievementBase):
    pass


class Achievement(AchievementBase):
    id: int
    earned: Optional[bool] = False

    class Config:
        orm_mode = True


# User Progress schemas
class UserProgressBase(BaseModel):
    user_id: int
    level_id: int
    is_completed: bool = False


class UserProgressCreate(UserProgressBase):
    pass


class UserProgress(UserProgressBase):
    id: int
    last_accessed: datetime

    class Config:
        orm_mode = True


# User Achievement schemas
class UserAchievementBase(BaseModel):
    user_id: int
    achievement_id: int


class UserAchievementCreate(UserAchievementBase):
    pass


class UserAchievement(UserAchievementBase):
    id: int
    earned_at: datetime

    class Config:
        orm_mode = True


# Quiz Attempt schemas
class QuizAttemptBase(BaseModel):
    user_id: int
    quiz_id: int
    score: float
    max_score: float
    points_earned: int


class QuizAttemptCreate(QuizAttemptBase):
    pass


class QuizAttempt(QuizAttemptBase):
    id: int
    completed_at: datetime

    class Config:
        orm_mode = True


# User response with gamification data
class UserWithGameData(UserBase):
    id: int
    is_active: bool
    current_level: int
    total_points: int
    experience_points: int
    created_at: datetime
    progress: List[UserProgress] = []
    achievements: List[UserAchievement] = []
    quiz_attempts: List[QuizAttempt] = []

    class Config:
        orm_mode = True


# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# Quiz submission schema
class QuizSubmission(BaseModel):
    quiz_id: int
    answers: Dict[int, int]  # question_id: selected_option_id


# Quiz result schema
class QuizResult(BaseModel):
    quiz_id: int
    score: float
    max_score: float
    points_earned: int
    correct_answers: Dict[int, bool]  # question_id: is_correct
    new_achievements: List[Achievement] = []
    level_up: bool = False
    new_level: Optional[int] = None


# Leaderboard entry schema
class LeaderboardEntry(BaseModel):
    id: int
    username: str
    total_points: int

    class Config:
        orm_mode = True
