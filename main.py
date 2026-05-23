from urllib import response
from wsgiref import headers

from fastapi import FastAPI, Request, HTTPException
import uvicorn
import logging
from app.Config.AppConfig import  settings
from app.Config.db import *
from app.router.user_router import router as user_router
from app.util.responses import send_error_response

app = FastAPI(
    title=settings.title,
    description=settings.description,
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")

app.include_router(user_router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # 1. Log the real error so you can debug it later in your terminal
    logging.error(f"Global exception caught: {str(exc)}", exc_info=True)

    # 2. Check if it's already an explicit FastAPI HTTPException
    if isinstance(exc, HTTPException):
        return send_error_response( data={
            "message":exc.detail,
            "status_code" : exc.status_code
        },
            status_code=exc.status_code,
            headers= dict(request.headers),
        )


@app.exception_handler(Exception)
async def global_generic_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unexpected System Crash: {str(exc)}", exc_info=True)

    return send_error_response(
        data={
            "message": "Internal server error",
            "status_code": 500
        },
        status_code=500,
        headers=dict(request.headers)
    )
@app.get("/")
async def root():
    return {"test": "Testing This Application"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="info")