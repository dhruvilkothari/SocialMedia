from fastapi import Request
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
    else:
        request.state.payload = None

    response = await call_next(request)
    return response