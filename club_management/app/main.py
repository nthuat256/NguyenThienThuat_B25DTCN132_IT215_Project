from fastapi import FastAPI
from app.db.database import Base, engine
from app.models import activity, club, user
from app.core.exception import http_exception_handler
from app.routers import activity as activity_router
from app.routers import auth, club as club_router, users
from fastapi import HTTPException

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_exception_handler(HTTPException, http_exception_handler)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(club_router.router)
app.include_router(activity_router.router)


@app.get("/health")
def health_check():
    return {
        "status": "hoạt động",
        "message": "API đang chạy"
    }