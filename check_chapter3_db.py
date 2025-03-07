from app.models import Achievement
from app.db import get_db

db = next(get_db())
try:
    print('Chapter 3 Achievements:')
    achievements = db.query(Achievement).filter(Achievement.chapter_id == 3).all()
    print(f'Found {len(achievements)} achievements for Chapter 3:')
    for a in achievements:
        print(f'- {a.title}: {a.description}')
finally:
    db.close()
