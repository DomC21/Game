from app.models import Achievement
from app.database import SessionLocal

db = SessionLocal()
try:
    print('Chapter 3 Achievements:')
    achievements = db.query(Achievement).filter(Achievement.chapter_id == 3).all()
    for a in achievements:
        print(f'- {a.title}: {a.description}')
finally:
    db.close()
