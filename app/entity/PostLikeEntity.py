from sqlalchemy import Table, Column, Integer, ForeignKey
from app.Config.db import Base


PostLikeEntity = Table(
    "post_likes",
    Base.metadata,

    Column(
        "user_id",
        Integer,
        ForeignKey("user_record.id"),
        primary_key=True
    ),

    Column(
        "post_id",
        Integer,
        ForeignKey("post_record.id"),
        primary_key=True
    ),
)