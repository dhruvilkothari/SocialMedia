from fastapi import HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc, asc
from sqlalchemy.orm import Session
import os
import uuid
import shutil
from app.Config.AppConfig import settings
from app.entity.CommentEntity import CommentEntity
from app.entity.PostEntity import PostEntity

from app.entity.UserEntity import UserEntity
from app.schema.post import PostDto
from typing import List

from app.util.responses import send_success_response


class PostService:
    def __init__(self, db: Session):
        self.db = db

    def create_post(
        self,
        post_dto: PostDto,
        file: UploadFile,
        user_id: int
    ):
        try:
            user_entity = (
                self.db.query(UserEntity)
                .filter(UserEntity.id == user_id)
                .first()
            )
            if not user_entity:
                raise HTTPException(
                    status_code=401,
                    detail="User not logged in"
                )
            post_dir = os.path.join(
                settings.directory,
                "../post"
            )
            os.makedirs(post_dir, exist_ok=True)
            _, ext = os.path.splitext(file.filename)
            new_filename = (
                f"{uuid.uuid4()}__userId_{user_entity.id}{ext}"
            )
            file_location = os.path.join(
                post_dir,
                new_filename
            )
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj( file.file, buffer)
            post_entity = PostEntity(title=post_dto.title, body=post_dto.body, picture=new_filename, owner_id=user_entity.id)
            self.db.add(post_entity)
            self.db.commit()
            self.db.refresh(post_entity)
            print("POST ENTITY is " , post_entity)
            return send_success_response(
                data={"record": jsonable_encoder(post_entity)},
                status_code=201
            )

        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )
        finally:
            file.file.close()

    def get_user_post(
            self,
            user_id: int,
            limit: int = 5,
            offset: int = 0,
            sortBy: str = "asc"
    ):
        try:
            query = (
                self.db.query(PostEntity)
                .filter(PostEntity.owner_id == user_id)
            )
            if sortBy.lower() == "desc":
                query = query.order_by(desc(PostEntity.created_at))
            else:
                query = query.order_by(asc(PostEntity.created_at))
            post_entity: List[PostEntity] = (query.offset(offset).limit(limit).all())
            return send_success_response(
                data={
                    "record": jsonable_encoder(post_entity)
                },
                status_code=200
            )
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    def get_post_by_id(self, user_id, post_id):
        try :
            post_entity: PostEntity | None = self.db.query(PostEntity).filter(
                PostEntity.id == post_id, PostEntity.owner_id == user_id
            ).first()

            if not post_entity:
                raise HTTPException(
                    status_code=404,
                    detail="Post Not Found For User"
                )
            return send_success_response(
                data={
                    "record": jsonable_encoder(post_entity)
                },
                status_code=200
            )
        except Exception as exp:
            print(exp)
            if isinstance(exp, HTTPException):
                raise HTTPException(status_code=exp.status_code, detail=exp.detail)

            raise HTTPException(status_code=500, detail="Internal Server Error")

    def like_or_dislike_post(self, user_id, post_id):
        try:
            user_entity: UserEntity = self.db.query(UserEntity).filter(
                UserEntity.id == user_id
            ).first()
            if not user_entity:
                raise HTTPException(
                    status_code=404,
                    detail="User not found"
                )
            post_entity: PostEntity | None = self.db.query(PostEntity).filter(
                PostEntity.id == post_id,
            ).first()
            if not post_entity:
                raise HTTPException(
                    status_code=404,
                    detail="Post Not Found"
                )
            if user_entity in post_entity.liked_by:
                post_entity.liked_by.remove(user_entity)
                post_entity.like_count-=1
            else:
                post_entity.liked_by.append(user_entity)
                post_entity.like_count+=1
            self.db.commit()
            self.db.refresh(post_entity)
            self.db.refresh(user_entity)
            return send_success_response(
                status_code=200,
                data=None
            )

        except Exception as exp:
            print(exp)
            if isinstance(exp, HTTPException):
                raise HTTPException(status_code=exp.status_code, detail=exp.detail)
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def add_comment(self, commentDto, post_id, user_id):

        try:
            post_entity: PostEntity | None = self.db.query(PostEntity).filter(
                PostEntity.id == post_id
            ).first()
            if post_entity is None:
                raise HTTPException(
                    status_code=404,
                    detail="Post Not Found"
                )
            user_entity: UserEntity | None = self.db.query(UserEntity).filter(
                UserEntity.id == user_id
            ).first()
            if user_entity is None:
                raise HTTPException(
                    status_code=404,
                    detail="User not found"
                )
            comment_entity: CommentEntity = CommentEntity(
                body=commentDto.body,
                user_id = user_id,
                post_id = post_id,
                parent_comment_id = None,
            )
            self.db.add(comment_entity)
            self.db.commit()
            self.db.refresh(comment_entity)
            return send_success_response(
                status_code=204,
                data=None
            )

        except Exception as exp:
            if isinstance(exp, HTTPException):
                raise HTTPException(status_code=exp.status_code, detail=exp.detail)
            raise HTTPException(status_code=500, detail="Internal Server Error")


