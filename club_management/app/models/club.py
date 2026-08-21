from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class Club(Base):
    __tablename__ = "clubs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    owner = relationship("User", back_populates="clubs_owned")
    members = relationship("ClubMember", back_populates="club", cascade="all, delete-orphan")
    activities = relationship("ClubActivity", back_populates="club", cascade="all, delete-orphan")

class ClubMember(Base):
    __tablename__ = "club_members"
    club_id = Column(Integer, ForeignKey("clubs.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role = Column(String(20), default="MEMBER")
    joined_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    club = relationship("Club", back_populates="members")
    user = relationship("User", back_populates="memberships")