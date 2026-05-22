from fastapi import FastAPI
import uvicorn
from app.Config.AppConfig import  settings
from app.Config.db import *



app = FastAPI(
    title=settings.title,
    description=settings.description,
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")


@app.get("/")
async def root():
    return {"test": "Testing This Application"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="info")