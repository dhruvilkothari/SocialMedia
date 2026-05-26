from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import relationship
from datetime import datetime
from app.Config.db import Base


class CommentEntity(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)

    body = Column(String(500), nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("user_record.id"),
        nullable=False
    )

    post_id = Column(
        Integer,
        ForeignKey("post_record.id"),
        nullable=False
    )

    # self reference
    parent_comment_id = Column(
        Integer,
        ForeignKey("comments.id"),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # owner
    user = relationship(
        "UserEntity",
        back_populates="comments"
    )
    post = relationship(
        "PostEntity",
        back_populates="comments"
    )
    replies = relationship(
        "CommentEntity",
        back_populates="parent_comment",
        cascade="all, delete-orphan"
    )
    parent_comment = relationship(
        "CommentEntity",
        remote_side=[id],
        back_populates="replies"
    )