from fastapi import FastAPI

from starlette.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.cache import ResourceManager
from app.config import conf
from app.router import admin_router, page_router, resource_router

# Start RM
ResourceManager()

app = FastAPI()

# Middleware
origins = [
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8000",
    "http://192.168.1.87:8000",
    "https://www.slaird.dev",
    "https://slaird.dev",
    "https://samlaird.com",
    "https://www.samlaird.com",
    "https://portfolio.alpine.slaird.dev"
]

app.add_middleware(
      CORSMiddleware,
      allow_origins=origins,
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
)

app.add_middleware(GZipMiddleware)
#app.add_middleware(BrotliMiddleware, gzip_fallback=True)



# Static Files
app.mount(conf.static_root, StaticFiles(directory=conf.static_dir), name="static")
editor_dir = f'{conf.static_dir}/res/js/editor'
app.mount('/res/app/editor', StaticFiles(directory=editor_dir), name="editor")


# Base router
app.include_router(page_router)
app.include_router(admin_router, prefix="/admin")
app.include_router(resource_router)

