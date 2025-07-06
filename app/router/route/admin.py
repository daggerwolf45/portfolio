from fastapi import APIRouter
from starlette.exceptions import HTTPException

from app.cache import ResourceManager

router = APIRouter()


@router.get('/reload')
async def reload_cache():
    # TODO restrict to local/signed-in users
    ResourceManager.reload_cache()
    return HTTPException(status_code=200)
