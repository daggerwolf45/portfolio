from typing import Annotated

from fastapi import APIRouter, Body, BackgroundTasks
from starlette.exceptions import HTTPException

from app.cache import ResourceManager, blog_stub
from app.config import conf
from app.md import RenderedMarkdown
from app.router.deps import standard_dep
from app.router.response import blog_response, page_response

router = APIRouter()


###
# Tools
#
@router.get('/reload')
@router.post('/reload')
async def reload_cache():
    # TODO restrict to local/signed-in users
    ResourceManager.reload_cache()
    return HTTPException(status_code=200)


###
# WWW
#
@router.get('')
async def hub(std: standard_dep):
    ResourceManager.reload_cache()
    return await page_response(
        std, "admin/hub", title='Internal Hub')


@router.get('/tools/mdedit')
async def mdedit(std: standard_dep, bg: BackgroundTasks):
    bg.add_task(ResourceManager.reload_cache)
    return await page_response(
          std, "mdedit", title='Blogspot', get_page_data=True)


@router.get('/view/isoblog/{blog_id}')
async def isoblog(std: standard_dep,blog_id: str):
    stub: blog_stub = None
    try:
        stub = ResourceManager.get_blog(blog_id)
    except:
        raise HTTPException(status_code=404)

    blog_path = conf.blog_dir / stub.filename

    markdown = RenderedMarkdown(path=blog_path)

    return await blog_response(std, markdown, isolated=True)


@router.post('/view/isoblog')
async def isoblog(std: standard_dep, blog: Annotated[str, Body()]):
    markdown = RenderedMarkdown(text=blog)
    return await blog_response(std, markdown, isolated=True)
