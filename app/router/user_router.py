from fastapi import Request, Response, APIRouter, Depends, HTTPException, File, UploadFile
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

@router.get("/me")
async def me(request: Request, service: UserService = Depends(get_user_service)):
    user_id = int(request.state.payload["id"])
    if not user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return service.get_my_profile(user_id)

@router.patch("/upload_profile")
async def upload_pic(req: Request, file: UploadFile = File(...), service: UserService = Depends(get_user_service)):
    user_id = int(req.state.payload["id"])
    if not user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return service.upload_pic(file, user_id)
