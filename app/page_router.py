from typing import Annotated, Optional

import humanize
from fastapi import BackgroundTasks, Depends, HTTPException

from fastapi import APIRouter
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates, _TemplateResponse

from app.cache import ResourceManager, blog_stub
from app.config import conf
from app.md import RenderedMarkdown
from app.models import Job
from app.utils import truncate

page_router = APIRouter()
admin_router = APIRouter()


class std_dep:
    request: Request
    blogs: list[tuple[str, str]]  #name, path
    last_blog: str

    def __init__(self, request: Request, blogs=Depends(ResourceManager.latest_blogs, use_cache=False)):
        self.request = request

        self.blogs = [(truncate(b.title, conf.nav_menu_char_limit), b.name) for b in blogs]
        self.last_blog = humanize.naturaltime(blogs[0].date)


standard_dep = Annotated[std_dep, Depends()]

jinja_loader = FileSystemLoader(conf.template_dir)
#jinja_ext = ['jinja2.ext.i18n.trimmed']
jinja_env = Environment(trim_blocks=True, lstrip_blocks=True, autoescape=True, loader=jinja_loader, enable_async=False)
templates = Jinja2Templates(env=jinja_env)


class TestAdvDep:
    def __call__(self, path:str = None) -> Optional[dict]:
        if path is None:
            print('No path!')
            return None
        print('<dep> Searching for:', path)
        return ResourceManager.get_page_data(path)


adv_dep = TestAdvDep()
use_page_data = Annotated[Optional[dict], Depends(adv_dep)]


async def template_response(request: Request, path:str, *, process_name=True, **kw) -> _TemplateResponse:
    if process_name and not path.endswith('.jinja2'):
        if path.endswith('.html'):
            path = f'{path}.jinja2'
        else:
            path = f'{path}.html.jinja2'

    context = kw
    try:
        return templates.TemplateResponse(request=request, name=path, context=context)
    except TemplateNotFound as e:
        raise e


async def page_response(common: std_dep, path: str, get_page_data: bool = True, *, title:str, **kw, ) -> _TemplateResponse:
    if get_page_data:
        kw['page'] = ResourceManager.get_page_data(path)

    kw['share_title'] = kw.get('share_title', title)
    real_path = common.request.url.path[:-1] + common.request.url.path[-1].replace('/','')
    canonical_url = conf.proxy_base + real_path

    return await template_response(
          request=common.request,
          path=path,
          title=title,
          latest_blogs=common.blogs,
          last_blog_published_time=common.last_blog,
          pageUrl=str(common.request.url),
          canonical_url=canonical_url,
          **kw
    )


async def blog_response(common: std_dep,  markdown: RenderedMarkdown, **kw) -> _TemplateResponse:
    return await page_response(
          common,
          "blog_base",
          md_content=markdown.html,
          md_toc=markdown.toc,
          **markdown.meta.__dict__,
          **kw
    )


# Routes
# Index
@page_router.get('/', response_class=HTMLResponse)
async def index(std: standard_dep, bg: BackgroundTasks):
    bg.add_task(ResourceManager.reload_cache)
    return await page_response(std, "index", True, title='Sam Laird',
                               description="Hi! I'm Sam Laird. This link takes you to my website. I got all sorts of things there like my portfolio, projects, photography and blog! Check it out!"
                               )
    #return await template_response(request, "index", title="Sam Laird", ptext="Hello World!", test_out=std.blogs)


# Portfolio
@page_router.get('/portfolio', response_class=HTMLResponse)
async def portfolio(std: standard_dep, experience: Annotated[list[Job], Depends(ResourceManager.get_all_exp)]):
    return await page_response(std, "portfolio", title='Sam Laird - Portfolio', experience=experience, share_title="Sam Laird's Portfolio")


@page_router.get('/portfolio-alt', response_class=HTMLResponse)
async def portfolio_alt(std: standard_dep):
    return await page_response(std, "portfolio-alt", title='Sam Laird - Portfolio')


# Works
@page_router.get('/works', response_class=HTMLResponse)
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
@page_router.get('/contact', response_class=HTMLResponse)
async def contact(std: standard_dep):
    return await page_response(std, "contact", True,  title='Sam Laird - Contacts', share_title='Contact Sam Laird')

# Testing page
@page_router.get('/demo', response_class=HTMLResponse)
async def contact(std: standard_dep):
    return await page_response(std, "demo", False,  title='Demo', share_title='Spooky scary secret page')

# Blog Posts
@page_router.get(conf.blog_root + '{blog_id}', response_class=HTMLResponse)
async def get_blog(std: standard_dep, blog_id: str):
    stub: blog_stub = None
    try:
        stub = ResourceManager.get_blog(blog_id)
    except:
        raise HTTPException(status_code=404)

    blog_path = conf.blog_dir / stub.filename

    markdown = RenderedMarkdown(path=blog_path)

    return await blog_response(std, markdown)



@admin_router.get('/reload')
async def reload_cache():
    # TODO restrict to local/signed-in users
    ResourceManager.reload_cache()
    return HTTPException(status_code=200)
