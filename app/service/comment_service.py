from fastapi.dependencies import models
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from app.entity.CommentEntity import CommentEntity
from app.entity.PostEntity import PostEntity
from app.entity.UserEntity import UserEntity
from app.util.responses import send_success_response


class CommentService:
    def __init__(self, db: Session):
        self.db = db

    def create_comment_inside_comment(self, comment_dto, post_id, user_id, comment_id):
        try:
            post_id = self.db.query(PostEntity).filter(PostEntity.id == post_id).first()
            if not post_id:
                raise HTTPException(status_code=404, detail="Post not found")
            user_id = self.db.query(UserEntity).filter(UserEntity.id == user_id).first()
            if not user_id:
                raise HTTPException(status_code=404, detail="User not found")
            comment_entity = self.db.query(CommentEntity).filter(CommentEntity.id == comment_id).first()
            if not comment_entity:
                raise HTTPException(status_code=404, detail="Comment not found")
            new_comment = CommentEntity(
                body=comment_dto.body,
                post_id=post_id,
                user_id=user_id,
                parent_id=comment_entity.id
            )
            self.db.add(new_comment)
            self.db.commit()
            self.db.refresh(new_comment)
            return send_success_response(
                status_code=204,
                data=None
            )


        except Exception as exp:
            if isinstance(exp, HTTPException):
                raise HTTPException(status_code=exp.status_code, detail=exp.detail)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        pass

