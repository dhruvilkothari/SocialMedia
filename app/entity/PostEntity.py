from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.Config.db import Base
class PostEntity(Base):
    __tablename__ = "post_record"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    body = Column(String(255), nullable=False)
    picture = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    like_count = Column(Integer, default=0)
    owner_id = Column(
        Integer,
        ForeignKey("user_record.id"),
        nullable=False
    )
    owner = relationship(
        "UserEntity",
        back_populates="posts"
    )
    class Config:
        from_attributes = True
