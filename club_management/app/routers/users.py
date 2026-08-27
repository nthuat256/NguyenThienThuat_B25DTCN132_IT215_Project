from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies import get_current_user, require_admin_or_manager
from app.models.user import User
from app.schemas.user import MeResponse, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=MeResponse)
def get_me(current_user: User = Depends(get_current_user)):
    account_age_days = (datetime.utcnow() - current_user.created_at).days
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at,
        "is_admin": current_user.role == "ADMIN",
        "account_age_days": max(account_age_days, 0),
    }


@router.get("/", response_model=list[UserResponse], dependencies=[Depends(require_admin_or_manager)])
def get_users(
    q: str | None = None,
    domain: str | None = None,
    is_active: bool | None = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    limit = min(max(limit, 1), 50)
    offset = max(offset, 0)

    query = db.query(User)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(User.email.ilike(like), User.full_name.ilike(like)))
    if domain:
        domain = domain.strip().lower().lstrip("@")
        query = query.filter(User.email.ilike(f"%@{domain}"))
    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    return query.offset(offset).limit(limit).all()
