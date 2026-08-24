from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.exception import (
    ClubNotFoundException,
    ClubOwnerRequiredException,
    UserAlreadyMemberException,
    UserNotFoundException,
)
from app.dependencies import get_current_user
from app.db.database import get_db
from app.models.club import Club, ClubMember
from app.models.user import User
from app.schemas.club import ClubCreate, ClubMemberCreate, ClubMemberResponse, ClubResponse, ClubUpdate

router = APIRouter(prefix='/clubs', tags=['clubs'])


def get_club(club_id: int, db: Session) -> Club:
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise ClubNotFoundException()
    return club


@router.post('/', response_model=ClubResponse, status_code=status.HTTP_201_CREATED)
def create_club(club_data: ClubCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    club = Club(**club_data.model_dump(), owner_id=current_user.id)
    db.add(club)
    db.commit()
    db.refresh(club)
    return club


@router.get('/', response_model=list[ClubResponse])
def get_clubs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Club).all()


@router.get('/{club_id}', response_model=ClubResponse)
def get_club_by_id(club_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_club(club_id, db)


@router.put('/{club_id}', response_model=ClubResponse)
def update_club(club_id: int, club_data: ClubUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    club = get_club(club_id, db)
    if club.owner_id != current_user.id:
        raise ClubOwnerRequiredException("update the club")
    for key, value in club_data.model_dump(exclude_unset=True).items():
        setattr(club, key, value)
    db.commit()
    db.refresh(club)
    return club


@router.delete('/{club_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_club(club_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    club = get_club(club_id, db)
    if club.owner_id != current_user.id:
        raise ClubOwnerRequiredException("delete the club")
    db.delete(club)
    db.commit()


@router.post('/{club_id}/members', response_model=ClubMemberResponse, status_code=status.HTTP_201_CREATED)
def add_member(club_id: int, member_data: ClubMemberCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    club = get_club(club_id, db)
    if club.owner_id != current_user.id:
        raise ClubOwnerRequiredException("add members")
    if not db.query(User).filter(User.id == member_data.user_id).first():
        raise UserNotFoundException()
    if db.query(ClubMember).filter(ClubMember.club_id == club_id, ClubMember.user_id == member_data.user_id).first():
        raise UserAlreadyMemberException()
    member = ClubMember(club_id=club_id, **member_data.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


@router.get('/{club_id}/members', response_model=list[ClubMemberResponse])
def get_members(club_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    get_club(club_id, db)
    return db.query(ClubMember).filter(ClubMember.club_id == club_id).all()
