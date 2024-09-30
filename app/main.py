from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.cache import ResourceManager
from app.config import conf
from app.page_router import page_router

ResourceManager()

app = FastAPI()

static_dir = conf.script_directory / "resources" / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.include_router(page_router)
