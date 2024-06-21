from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from . import crud, schemas
from datetime import datetime, timedelta, timezone

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler(timezone=f'Asia/Jakarta')
    scheduler.add_job(func=crud.delete_expired_pastes, trigger='interval', seconds=60)
    scheduler.start()
    yield

app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/create", response_class=HTMLResponse)
async def create_paste(request: Request, content: str = Form(...), burn_after_reading: bool = Form(False), expires_in: int = Form(...)):
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_in)
    paste = schemas.PasteCreate(content=content, burn_after_reading=burn_after_reading, expired_at=expires_at)
    paste_id = await crud.create_paste(paste)
    paste_url = request.url_for('read_paste', id=paste_id)
    return templates.TemplateResponse("paste_created.html", {"request": request, "paste_url": paste_url})

@app.get("/paste/{id}", response_class=HTMLResponse)
async def read_paste(request: Request, id: str):
    paste = await crud.get_paste(id)
    if paste:
        if paste.burn_after_reading:
            await crud.delete_paste(id)
        return templates.TemplateResponse("paste.html", {"request": request, "paste": paste})
    return RedirectResponse(url="/")
