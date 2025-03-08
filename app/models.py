from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Gamification fields
    current_level = Column(Integer, default=1)
    total_points = Column(Integer, default=0)
    experience_points = Column(Integer, default=0)
    
    # Relationships
    progress = relationship("UserProgress", back_populates="user")
    achievements = relationship("UserAchievement", back_populates="user")
    quiz_attempts = relationship("QuizAttempt", back_populates="user")


class Level(Base):
    __tablename__ = "levels"
    
    id = Column(Integer, primary_key=True, index=True)
    level_number = Column(Integer, unique=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    required_points = Column(Integer)
    is_locked = Column(Boolean, default=True)
    
    # Relationships
    chapters = relationship("Chapter", back_populates="level")


class Chapter(Base):
    __tablename__ = "chapters"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    order = Column(Integer)
    level_id = Column(Integer, ForeignKey("levels.id"))
    
    # Relationships
    level = relationship("Level", back_populates="chapters")
    quizzes = relationship("Quiz", back_populates="chapter")


class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    points_reward = Column(Integer, default=10)
    quiz_type = Column(String, default="regular")  # "regular", "boss_fight", "mini_challenge"
    chapter_id = Column(Integer, ForeignKey("chapters.id"))
    
    # Relationships
    chapter = relationship("Chapter", back_populates="quizzes")
    questions = relationship("Question", back_populates="quiz")
    attempts = relationship("QuizAttempt", back_populates="quiz")


class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text)
    explanation = Column(Text, nullable=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    
    # Relationships
    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("QuestionOption", back_populates="question")


class QuestionOption(Base):
    __tablename__ = "question_options"
    
    id = Column(Integer, primary_key=True, index=True)
    option_text = Column(Text)
    is_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey("questions.id"))
    
    # Relationships
    question = relationship("Question", back_populates="options")


class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    badge_image = Column(String)  # Path to badge image
    requirement_type = Column(String)  # e.g., "quiz_score", "level_complete", "points_earned"
    requirement_value = Column(Integer)  # Value needed to earn achievement
    chapter_id = Column(Integer, nullable=True)  # Optional chapter ID for chapter-specific achievements
    
    # Relationships
    user_achievements = relationship("UserAchievement", back_populates="achievement")


class UserProgress(Base):
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    level_id = Column(Integer, ForeignKey("levels.id"))
    is_completed = Column(Boolean, default=False)
    last_accessed = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="progress")
    level = relationship("Level")


class UserAchievement(Base):
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    achievement_id = Column(Integer, ForeignKey("achievements.id"))
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    score = Column(Float)
    max_score = Column(Float)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    points_earned = Column(Integer)
    
    # Relationships
    user = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")


class QuizAnswer(Base):
    __tablename__ = "quiz_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    selected_option_id = Column(Integer, ForeignKey("question_options.id"))
    is_correct = Column(Boolean, default=False)
    answered_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    question = relationship("Question")
    selected_option = relationship("QuestionOption")


class SpecialQuizAchievementRequirement(Base):
    __tablename__ = "special_quiz_achievement_requirements"
    
    id = Column(Integer, primary_key=True, index=True)
    achievement_id = Column(Integer, ForeignKey("achievements.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    
    # Relationships
    achievement = relationship("Achievement")
    question = relationship("Question")
