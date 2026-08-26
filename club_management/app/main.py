from fastapi import FastAPI, HTTPException

from app.core.exception import http_exception_handler
from app.db.database import Base, engine
from app.routers import auth, club as club_router, users
from app.routers.activity import activity_router, club_activity_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Club Management API",
    description="API quản lý câu lạc bộ, thành viên và hoạt động với JWT Authentication và phân quyền.",
    version="1.0.0",
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(club_router.router)
app.include_router(club_activity_router)
app.include_router(activity_router)


@app.get(
    "/health",
    tags=["system"],
    summary="Kiểm tra trạng thái API",
)
def health_check():
    return {
        "status": "hoạt động",
        "message": "API đang chạy",
    }