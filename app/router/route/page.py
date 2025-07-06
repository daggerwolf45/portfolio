from typing import Annotated, Optional

from fastapi import BackgroundTasks, Depends, HTTPException

from fastapi import APIRouter
from starlette.responses import HTMLResponse

from app.cache import ResourceManager, blog_stub
from app.config import conf
from app.md import RenderedMarkdown
from app.models import Job
from app.router.deps import standard_dep
from app.router.response import blog_response, page_response
from app.utils import truncate


router = APIRouter()


# Routes
# Index
@router.get('/', response_class=HTMLResponse)
async def index(std: standard_dep, bg: BackgroundTasks):
    bg.add_task(ResourceManager.reload_cache)
    return await page_response(std, "index", True, title='Sam Laird',
                               description="Hi! I'm Sam Laird. This link takes you to my website. I got all sorts of things there like my portfolio, projects, photography and blog! Check it out!"
                               )
    #return await template_response(request, "index", title="Sam Laird", ptext="Hello World!", test_out=std.blogs)


# Portfolio
@router.get('/portfolio', response_class=HTMLResponse)
async def portfolio(std: standard_dep, experience: Annotated[list[Job], Depends(ResourceManager.get_all_exp)]):
    return await page_response(std, "portfolio", title='Sam Laird - Portfolio', experience=experience, share_title="Sam Laird's Portfolio")


@router.get('/portfolio-alt', response_class=HTMLResponse)
async def portfolio_alt(std: standard_dep):
    return await page_response(std, "portfolio-alt", title='Sam Laird - Portfolio')


# Works
@router.get('/works', response_class=HTMLResponse)
async def works(std: standard_dep, blogs: Annotated[list[blog_stub], Depends(ResourceManager.latest_blogs)]):
    blogs = [
        (
            truncate(b.title, conf.works_blog_char_limit),
            b.name,
            b.author,
            truncate(b.description, conf.works_blog_desc_char_limit),
        ) for b in blogs]

    return await page_response(std, "works", title='Things I made - Sam Laird', blogs=blogs)


# Contact
@router.get('/contact', response_class=HTMLResponse)
async def contact(std: standard_dep):
    return await page_response(std, "contact", True,  title='Sam Laird - Contacts', share_title='Contact Sam Laird')


# Testing page
@router.get('/demo', response_class=HTMLResponse)
async def contact(std: standard_dep):
    cards = [
        {
            "name": "A post",
            "desc": "This is a card!",
            "img": ""
        }
    ]

    return await page_response(std, "demo", True,  title='Demo', share_title='Spooky scary secret page')


# Blog Posts
@router.get(conf.blog_root + '{blog_id}', response_class=HTMLResponse)
async def get_blog(std: standard_dep, blog_id: str):
    stub: blog_stub = None
    try:
        stub = ResourceManager.get_blog(blog_id)
    except:
        raise HTTPException(status_code=404)

    blog_path = conf.blog_dir / stub.filename

    markdown = RenderedMarkdown(path=blog_path)

    return await blog_response(std, markdown)
