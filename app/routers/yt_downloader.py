from tempfile import mkdtemp
from typing import Annotated
import uuid
from fastapi import APIRouter, BackgroundTasks, Form, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from yt_dlp import YoutubeDL
from urllib.parse import quote

router = APIRouter(prefix="/youtube", tags=["youtube"])

# Remember to make a check that if the sponserblock request doesn't go through , prompt the user to download with Ads or wait till sponser block is back

file_registry: dict[str, str] = {}

class FormData(BaseModel):
    url: str
    
@router.post("/create")
async def download_youtube_video(data: Annotated[FormData, Form()]):

    tmpdir = mkdtemp()

    ydl_opts = {
        "format": "bestaudio/best",
        "cookiesfrombrowser": ('firefox',),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            },
            {"key": "SponsorBlock"},
            {"key": "ModifyChapters", "remove_sponsor_segments": ["sponsor", "selfpromo"]},
        ],
        "outtmpl": f"{tmpdir}/%(title)s.%(ext)s",
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(data.url, download=True)
        video_title = info.get("title", "audio")

    if not info:
        raise HTTPException(status_code=503, detail="Couldn't download the video")

    token = str(uuid.uuid4())
    file_registry[token] = tmpdir
    
    return {"path": token, "title": video_title}


@router.get("/download")
async def downloadYoutubeAudio(path: str, title: str, background_task: BackgroundTasks):

    # run a background task to clear file
    # run CRON job to clean up left over files after download
    print(file_registry)
    tmpdir = file_registry.get(path)
    del file_registry[path]
    
    return FileResponse(path=f"{tmpdir}/{title}.mp3", filename=title, media_type="audio/mpeg", headers={"Content-Disposition": f'attachment; filename="{quote(title)}.mp3"'})
