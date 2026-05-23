import uuid

from fastapi import HTTPException, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import asyncio
import shutil
import os
from app.Config.AppConfig import settings
from app.entity.UserEntity import UserEntity
from app.schema.user_dto import UserDto, UserLogin
from app.util.jwt import create_access_token
from app.util.password import get_password_hash, verify_password
from app.util.responses import send_success_response


class UserService:
    def __init__(self, db: Session):
        self.db = db
    def get_user_response(self, user_entity: UserEntity)->dict:
        response_data = {
            "id": user_entity.id,
            "email": user_entity.email,
            "name": user_entity.name,
            "profile_pic": user_entity.profile_pic,
            "created_at": user_entity.created_at.isoformat(),
            "updated_at": user_entity.updated_at.isoformat(),
            "is_active": user_entity.is_active,
        }
        return response_data

    def create_user(self, user_dto: UserDto):
        try :
            user_entity = UserEntity(
                name=user_dto.name,
                email=user_dto.email,
                password=get_password_hash(user_dto.password),

            )
            self.db.add(user_entity)
            self.db.commit()
            self.db.refresh(user_entity)

            return send_success_response({"record": self.get_user_response(user_entity)})
        except IntegrityError as e:
            print(e)
            self.db.rollback()
            raise HTTPException(status_code=400, detail="User already exists or database constraint failed")
        except Exception as e:
            print(e)
            print(f"Database integrity issue: {e}")
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")

    def login_user(self, user_login: UserLogin):

        try :
            email, password = user_login.email, user_login.password
            user_entity = self.db.query(UserEntity).filter(UserEntity.email == email).first()
            if not user_entity:
                raise HTTPException(status_code=400, detail="User does not exist")
            is_valid_user = verify_password(password, user_entity.password)
            if not is_valid_user:
                raise HTTPException(status_code=403, detail="Incorrect password/name")
            return send_success_response({"record": self.get_user_response(user_entity), "token": create_access_token({"id": user_entity.id})})

        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail="Internal server error")

    def get_my_profile(self, user_id):
        try:
            user_entity = self.db.query(UserEntity).filter(UserEntity.id == user_id).first()
            return send_success_response({"record": self.get_user_response(user_entity)})
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail="Internal server error")

    def delete_old_pic(self, path: str):
        if path and os.path.exists(path):
            os.remove(path)

    def upload_pic(self, file, user_id, bg: BackgroundTasks = None):
        try:
            user_entity: UserEntity = self.db.query(UserEntity).filter(UserEntity.id == user_id).first()

            if not user_entity:
                raise HTTPException(
                    status_code=404,
                    detail="User does not exist"
                )
            old_pic = user_entity.profile_pic
            _, ext = os.path.splitext(file.filename)
            new_filename = f"{uuid.uuid4()}__userId_{user_id}{ext}"
            file_location = os.path.join(
                settings.directory,
                new_filename
            )
            with open(file_location, "wb+") as file_object:
                shutil.copyfileobj(file.file, file_object)

            # update DB
            user_entity.profile_pic = new_filename
            self.db.commit()
            self.db.refresh(user_entity)
            if bg and old_pic:
                old_path = os.path.join(
                    settings.directory,
                    old_pic
                )
                bg.add_task(self.delete_old_pic, old_path)

            return send_success_response(
                {"record": self.get_user_response(user_entity)}
            )

        except Exception as e:
            print(e)
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )

    def update_profile(self, user_update, user_id):
        try:
            user_entity: UserEntity = self.db.query(UserEntity).filter(UserEntity.id == user_id).first()
            if not user_entity:
                raise HTTPException(status_code=404, detail="User does not exist")
            user_update_dict = user_update.dict(exclude_unset=True)
            for key, value in user_update_dict.items():
                if key == "password":
                    setattr(user_entity, key, get_password_hash(value))
                else:
                    setattr(user_entity, key, value)
            self.db.commit()
            self.db.refresh(user_entity)
            return send_success_response({"record": self.get_user_response(user_entity)})
        except Exception as e:
            print(e)
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )


