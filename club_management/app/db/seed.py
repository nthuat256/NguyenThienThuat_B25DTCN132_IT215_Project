from app.db.database import SessionLocal
from app.models.club import Club, ClubMember
from app.models.activity import ClubActivity
from app.models.user import User
from app.core.security import get_password_hash


def get_or_create(db, model, filter_by: dict, **kwargs):
    instance = db.query(model).filter_by(**filter_by).first()
    if not instance:
        instance = model(**{**filter_by, **kwargs})
        db.add(instance)
        db.commit()
        db.refresh(instance)
    return instance


def seed_data():
    with SessionLocal() as db:
        admin = get_or_create(
            db,
            User,
            {"email": "admin@gmail.com"},
            password_hash=get_password_hash("demo_password"),
            full_name="Admin",
            role="ADMIN",
            is_active=True,
        )

        user1 = get_or_create(
            db,
            User,
            {"email": "nguyenvana@gmail.com"},
            password_hash=get_password_hash("demo_password"),
            full_name="Nguyen Van A",
            role="USER",
            is_active=True,
        )

        user2 = get_or_create(
            db,
            User,
            {"email": "tranthib@gmail.com"},
            password_hash=get_password_hash("demo_password"),
            full_name="Tran Thi B",
            role="USER",
            is_active=True,
        )

        user3 = get_or_create(
            db,
            User,
            {"email": "levanc@gmail.com"},
            password_hash=get_password_hash("demo_password"),
            full_name="Le Van C",
            role="USER",
            is_active=True,
        )

        user4 = get_or_create(
            db,
            User,
            {"email": "phamthid@gmail.com"},
            password_hash=get_password_hash("demo_password"),
            full_name="Pham Thi D",
            role="USER",
            is_active=True,
        )

        python_club = get_or_create(
            db,
            Club,
            {"name": "Python Club"},
            description="Cau lac bo lap trinh Python va FastAPI",
            owner_id=admin.id,
        )

        web_club = get_or_create(
            db,
            Club,
            {"name": "Web Development Club"},
            description="Cau lac bo phat trien ung dung Web",
            owner_id=user1.id,
        )

        data_club = get_or_create(
            db,
            Club,
            {"name": "Data Science Club"},
            description="Cau lac bo Data Analysis va Machine Learning",
            owner_id=user2.id,
        )

        members = [
            (python_club.id, user1.id, "MEMBER"),
            (python_club.id, user2.id, "MEMBER"),
            (python_club.id, user3.id, "MEMBER"),
            (web_club.id, user2.id, "MEMBER"),
            (web_club.id, user3.id, "MEMBER"),
            (web_club.id, user4.id, "MEMBER"),
            (data_club.id, user3.id, "MEMBER"),
            (data_club.id, user4.id, "MEMBER"),
            (data_club.id, admin.id, "MEMBER"),
        ]

        for club_id, user_id, role in members:
            get_or_create(
                db,
                ClubMember,
                {"club_id": club_id, "user_id": user_id},
                role=role,
            )

        activities = [
            {
                "club_id": python_club.id,
                "title": "FastAPI Workshop",
                "description": "Buoi hoc FastAPI co ban",
                "status": "TODO",
                "priority": "HIGH",
                "assignee_id": user1.id,
            },
            {
                "club_id": python_club.id,
                "title": "Python Basic Practice",
                "description": "On tap Python co ban cho thanh vien moi",
                "status": "IN_PROGRESS",
                "priority": "MEDIUM",
                "assignee_id": user2.id,
            },
            {
                "club_id": python_club.id,
                "title": "Build CRUD API",
                "description": "Thuc hanh CRUD API voi FastAPI va SQLAlchemy",
                "status": "DONE",
                "priority": "HIGH",
                "assignee_id": user3.id,
            },
            {
                "club_id": web_club.id,
                "title": "HTML CSS Workshop",
                "description": "Thuc hanh giao dien Web co ban",
                "status": "TODO",
                "priority": "MEDIUM",
                "assignee_id": user2.id,
            },
            {
                "club_id": web_club.id,
                "title": "JavaScript Practice",
                "description": "Thuc hanh JavaScript va xu ly DOM",
                "status": "IN_PROGRESS",
                "priority": "HIGH",
                "assignee_id": user3.id,
            },
            {
                "club_id": data_club.id,
                "title": "Data Analysis Workshop",
                "description": "Lam quen voi Pandas va xu ly du lieu",
                "status": "TODO",
                "priority": "HIGH",
                "assignee_id": user4.id,
            },
            {
                "club_id": data_club.id,
                "title": "SQL Practice",
                "description": "Thuc hanh SELECT JOIN GROUP BY va HAVING",
                "status": "DONE",
                "priority": "MEDIUM",
                "assignee_id": user3.id,
            },
        ]

        for activity in activities:
            get_or_create(
                db,
                ClubActivity,
                {"title": activity["title"]},
                club_id=activity["club_id"],
                description=activity["description"],
                status=activity["status"],
                priority=activity["priority"],
                assignee_id=activity["assignee_id"],
            )

        print("Da seed du lieu mau thanh cong!")
        print("Tai khoan: admin@gmail.com / demo_password")
        print("Tai khoan USER: nguyenvana@gmail.com, tranthib@gmail.com, levanc@gmail.com, phamthid@gmail.com")
        print("Mat khau tat ca tai khoan: demo_password")


if __name__ == "__main__":
    seed_data()
