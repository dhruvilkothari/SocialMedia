from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException

from app.Config.db import get_db
from app.schema.comment import CommentDto
from app.service.comment_service import CommentService

router = APIRouter(
    prefix="/comment",
    tags=["comment"],
    responses={404: {"description": "Not found"}},
)

def get_post_service(db: Session = Depends(get_db)):
    return CommentService(db)

@router.post("/{comment_id}/post/{post_id}", tags=["comment"])

async def comment_post(req: Request,comment_id: int, comment_dto: CommentDto, post_id: int, service: CommentService = Depends(get_post_service)):
    try:

        user_id = int(req.state.payload["id"])
        if not user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User Not Logged In")
        return service.create_comment_inside_comment(comment_dto, post_id, user_id, comment_id)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise HTTPException(status_code=e.status_code, detail=str(e))

