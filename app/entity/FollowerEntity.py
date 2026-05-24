from sqlalchemy import Table, Column, Integer, ForeignKey
from app.Config.db import Base

followers = Table(
    "followers",
    Base.metadata,
    Column(
        "follower_id",
        Integer,
        ForeignKey("user_record.id"),
        primary_key=True
    ),
    Column(
        "following_id",
        Integer,
        ForeignKey("user_record.id"),
        primary_key=True
    )
)