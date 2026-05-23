from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
import os
import uuid
import shutil
from app.Config.AppConfig import settings
from app.entity.PostEntity import PostEntity

from app.entity.UserEntity import UserEntity
from app.schema.post import PostDto


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

            # save binary file
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(
                    file.file,
                    buffer
                )
            post_entity = PostEntity(
                title=post_dto.title,
                body=post_dto.body,
                picture=new_filename,
                owner_id=user_entity.id
            )
            self.db.add(post_entity)
            self.db.commit()
            self.db.refresh(post_entity)

            return post_entity

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