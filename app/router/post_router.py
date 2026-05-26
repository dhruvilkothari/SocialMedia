from fastapi import (
    APIRouter,
    Request,
    UploadFile,
    File,
    Form,
    Depends,
    HTTPException, Query
)
from typing import Literal
from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException

from app.Config.db import get_db
from app.schema.comment import CommentDto
from app.schema.post import PostDto
from app.service.post_service import PostService

posts_router = APIRouter(
    prefix="/api/v1/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)

def get_post_service(db: Session = Depends(get_db)):
    return PostService(db)


@posts_router.post("/create")
async def create_post(
    req: Request,
    title: str = Form(...),
    body: str = Form(...),
    picture: UploadFile = File(...),
    service: PostService = Depends(get_post_service)
):
    user_id = int(req.state.payload["id"])
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN
        )
    post_dto = PostDto(
        title=title,
        body=body
    )
    return service.create_post(
        post_dto=post_dto,
        file=picture,
        user_id=user_id
    )

@posts_router.get("/all")
async def get_all_posts(
    req: Request,
    limit: int = Query(default=5, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    sort_by: Literal["asc", "desc"] = Query(default="asc"),
    service: PostService = Depends(get_post_service)
):
    user_id = int(req.state.payload["id"])
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN
        )
    return service.get_user_post(user_id=user_id, limit=limit, offset=offset, sortBy=sort_by)

@posts_router.get("/user/{post_id}")
async def get_user_post_by_id(
    req: Request, post_id: int, service: PostService = Depends(get_post_service)
) -> dict | None:
    user_id = int(req.state.payload["id"])
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User Not Logged In"
        )
    return service.get_post_by_id(user_id=user_id, post_id=post_id)

@posts_router.post("/{post_id}/like")
async def like_post(req: Request, post_id: int, service: PostService = Depends(get_post_service)):
    user_id = int(req.state.payload["id"])
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User Not Logged In"
        )
    return service.like_or_dislike_post(user_id=user_id, post_id=post_id)

@posts_router.post("/{post_id}/comment}")
async def comment_post(
        req: Request, post_id: int, commentDto: CommentDto, service: PostService = Depends(get_post_service),
):
    try :
        user_id = int(req.state.payload["id"])
    except Exception as e :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User Not Logged In"
        )

    return service.add_comment(commentDto=commentDto, post_id=post_id, user_id= user_id)