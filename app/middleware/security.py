from fastapi import Request, HTTPException
from starlette import status

from app.util.jwt import verify_token   # renamed from jwt.py ideally


async def get_token(request: Request, call_next):
    auth_header = request.headers.get("Authorization")

    if auth_header and auth_header.startswith("Bearer "):
        try:
            payload = verify_token(request)
            request.state.payload = payload
            print(f"Payload: {payload}")
        except Exception:
            request.state.payload = None
            print(f"In Exception Block")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        request.state.payload = None

    response = await call_next(request)
    return response