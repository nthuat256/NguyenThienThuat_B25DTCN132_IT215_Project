from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_current_user
from app.db.database import get_db
from app.models.activity import ClubActivity
from app.models.club import Club
from app.models.user import User
from app.schemas.activity import ActivityCreate, ActivityResponse, ActivityUpdate

router = APIRouter(prefix='/clubs/{club_id}/activities', tags=['activities'])

def get_activity(club_id: int, activity_id: int, db: Session):
	activity = db.query(ClubActivity).filter(
		ClubActivity.id == activity_id,
		ClubActivity.club_id == club_id,
	).first()
	if not activity:
		raise HTTPException(status_code=404, detail='Activity not found')
	return activity

def check_club(club_id: int, db: Session, current_user: User):
	club = db.query(Club).filter(Club.id == club_id).first()
	if not club:
		raise HTTPException(status_code=404, detail='Club not found')
	if club.owner_id != current_user.id:
		raise HTTPException(status_code=403, detail='Only the club owner can manage activities')

@router.post('/', response_model=ActivityResponse, status_code=201)
def create_activity(club_id: int, activity_data: ActivityCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	check_club(club_id, db, current_user)
	activity = ClubActivity(club_id=club_id, **activity_data.model_dump())
	db.add(activity)
	db.commit()
	db.refresh(activity)
	return activity

@router.get('/', response_model=list[ActivityResponse])
def get_activities(club_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	check_club(club_id, db, current_user)
	return db.query(ClubActivity).filter(ClubActivity.club_id == club_id).all()

@router.get('/{activity_id}', response_model=ActivityResponse)
def get_activity_by_id(club_id: int, activity_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	check_club(club_id, db, current_user)
	return get_activity(club_id, activity_id, db)

@router.put('/{activity_id}', response_model=ActivityResponse)
def update_activity(club_id: int, activity_id: int, activity_data: ActivityUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	check_club(club_id, db, current_user)
	activity = get_activity(club_id, activity_id, db)
	for key, value in activity_data.model_dump(exclude_unset=True).items():
		setattr(activity, key, value)
	db.commit()
	db.refresh(activity)
	return activity

@router.delete('/{activity_id}', status_code=204)
def delete_activity(club_id: int, activity_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	check_club(club_id, db, current_user)
	db.delete(get_activity(club_id, activity_id, db))
	db.commit()