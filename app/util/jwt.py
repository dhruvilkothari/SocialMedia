from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, Request, status

from app.Config.AppConfig import settings
import logging

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_expiry
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )

    return encoded_jwt


def verify_token(req: Request):
    try:
        logging.log(logging.INFO, "Verifying token")
        auth_header = req.headers.get("Authorization")
        print("Auth Header: ", auth_header)
        if not auth_header:
            print("Auth Header is empty")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication credentials were not provided."
            )

        # Expect: Bearer <token>
        parts = auth_header.split()

        if len(parts) != 2 or parts[0] != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header."
            )

        token = parts[1]

        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )