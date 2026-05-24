from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from app.Config.db import Base
from sqlalchemy.orm import relationship
from app.entity.FollowerEntity import followers
from app.entity.PostLikeEntity import PostLikeEntity


class UserEntity(Base):
    __tablename__ = "user_record"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)

    email = Column(String(255), unique=True, index=True, nullable=False)

    password = Column(String(255), nullable=False)

    profile_pic = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    following = relationship(
        "UserEntity",
        secondary=followers,
        primaryjoin=id == followers.c.follower_id,
        secondaryjoin=id == followers.c.following_id,
        back_populates="followers"
    )

    followers = relationship(
        "UserEntity",
        secondary=followers,
        primaryjoin=id == followers.c.following_id,
        secondaryjoin=id == followers.c.follower_id,
        back_populates="following"
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    posts = relationship(
        "PostEntity",
        back_populates="owner",
        cascade="all, delete-orphan"
    )
    liked_posts = relationship(
        "PostEntity",
        secondary=PostLikeEntity,
        back_populates="liked_by"
    )

    def __repr__(self):
        return f"{self.name} - {self.email} following = {self.following}  followe = {self.followers}"
