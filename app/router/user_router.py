from fastapi import Request, Response, APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette import status

from app.Config.db import get_db
from app.schema.user_dto import UserDto, UserLogin
from app.service.user_service import UserService
from app.util.responses import send_success_response

def get_user_service(db: Session = Depends(get_db))->UserService:
    return UserService(db)

router = APIRouter(
    prefix="/api/v1/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_root(request: Request):
    return send_success_response({"message": "Hello World"}, status_code=status.HTTP_200_OK)

@router.post("/create")
async def create_user(request: Request, user_dto: UserDto, service: UserService = Depends(get_user_service)):
    return service.create_user(user_dto)

@router.post("/login")
async def login_user(request: Request, user_login: UserLogin, service: UserService = Depends(get_user_service)):
    return service.login_user(user_login)