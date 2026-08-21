from app.db.database import SessionLocal
from app.models.club import Club
from app.models.activity import ClubActivity
from app.models.user import User

def get_or_create(db, model, filter_by: dict,):
    instance = db.query(model).filter_by(**filter_by).first()
    if not instance:
        instance = model(**filter_by)
        db.add(instance)
        db.commit()
        db.refresh(instance)
    return instance


def seed_data():
    with SessionLocal() as db:
        user = get_or_create(
            db,
            User,
            {"email": "admin@gmail.com"},
            password_hash="demo_password",
            full_name="Admin",
            role="ADMIN",
        )

        club = get_or_create(
            db,
            Club,
            {"name": "Python Club"},
            description="Câu lạc bộ lập trình Python",
            owner_id=user.id,
        )

        get_or_create(
            db,
            ClubActivity,
            {"title": "FastAPI Workshop"},
            club_id=club.id,
            description="Buổi học FastAPI cơ bản",
            status="TODO",
            priority="HIGH",
        )


if __name__ == "__main__":
    seed_data()