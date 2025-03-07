from app.db import SessionLocal
from app import models

db = SessionLocal()
try:
    print('Chapter 4 Achievements:')
    achievements = db.query(models.Achievement).filter(models.Achievement.chapter_id == 4).all()
    print(f'Found {len(achievements)} achievements for Chapter 4:')
    for a in achievements:
        print(f'- {a.title}: {a.description}')
finally:
    db.close()
