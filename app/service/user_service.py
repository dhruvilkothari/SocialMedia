from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import asyncio
from app.entity.UserEntity import UserEntity
from app.schema.user_dto import UserDto, UserLogin
from app.util.password import get_password_hash, verify_password
from app.util.responses import send_success_response


class UserService:
    def __init__(self, db: Session):
        self.db = db

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

    def login_user(self, user_login: UserLogin):

        try :
            email, password = user_login.email, user_login.password
            user_entity = self.db.query(UserEntity).filter(UserEntity.email == email).first()
            if not user_entity:
                raise HTTPException(status_code=400, detail="User does not exist")
            is_valid_user = verify_password(password, user_entity.password)
            if not is_valid_user:
                raise HTTPException(status_code=400, detail="Incorrect password/name")
            response_data = {
                "id": user_entity.id,
                "email": user_entity.email,
                "name": user_entity.name,
                "profile_pic": user_entity.profile_pic,
                "created_at": user_entity.created_at.isoformat(),
                "updated_at": user_entity.updated_at.isoformat(),
                "is_active": user_entity.is_active,
            }
            return send_success_response({"record": response_data})

        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail="Internal server error")




