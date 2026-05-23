from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import asyncio
from app.entity.UserEntity import UserEntity
from app.schema.user_dto import UserDto
from app.util.responses import send_success_response


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_dto: UserDto):
        try :
            user_entity = UserEntity(
                name=user_dto.name,
                email=user_dto.email,
                password=user_dto.password,

            )
            self.db.add(user_entity)
            self.db.commit()
            self.db.refresh(user_entity)
            response_data = {
                "id": user_entity.id,
                "email": user_entity.email,
                "name": user_entity.name,
                "profile_pic": user_entity.profile_pic,
                "created_at": user_entity.created_at.isoformat(),
                "updated_at": user_entity.updated_at.isoformat(),
                "is_active": user_entity.is_active,
            }
            return send_success_response({"record":response_data})
        except IntegrityError as e:
            print(e)
            self.db.rollback()
            raise HTTPException(status_code=400, detail="User already exists or database constraint failed")
        except Exception as e:
            print(e)
            print(f"Database integrity issue: {e}")
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")

