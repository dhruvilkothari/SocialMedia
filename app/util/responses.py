from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Any

from app.schema.api_response import ApiResponse


def send_success_response(data: Any, status_code: int = 200, headers: dict = None) -> Any:
    return JSONResponse(
        content=jsonable_encoder(ApiResponse(data=data, status_code=status_code)),
        status_code=status_code,
    )

def send_error_response(data: Any, status_code: int = 500, headers: dict = None) -> Any:
    return JSONResponse(
        content=jsonable_encoder(ApiResponse(data=data, status_code=status_code, additional_data = {"headers": headers})),
        status_code=status_code,
    )
