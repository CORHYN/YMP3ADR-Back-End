from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import yt_downloader
from .config import settings


app = FastAPI()

origins = [
    settings.allowed_origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(yt_downloader.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
